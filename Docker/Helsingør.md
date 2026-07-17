# "Helsingør": The first walls of postgres physical replication

**Date** : 17/07/2026
**Difficulté** : moyen

## TL;DR
Réplique bloquée en boucle de restart car ses paramètres (max_connections, max_worker_processes, max_wal_senders, max_locks_per_transaction) étaient inférieurs à ceux du primaire. Corrigé dans postgres.conf de la réplique.

---

## Description
Vous configurez une base de données PostgreSQL avec réplication et vous avez opté pour Docker et Docker Compose afin de simplifier la gestion et les tests. Après quelques heures de travail, la base de données principale est opérationnelle, mais vous rencontrez des difficultés avec la réplique.

Vous devez identifier et résoudre le problème de la réplique.

Grâce à Docker Compose, vous pouvez vérifier l'état des conteneurs en cours d'exécution avec la commande `docker compose ps` (ou `docker ps`). Il est également conseillé de consulter les journaux des conteneurs.

Toutes les définitions des conteneurs se trouvent dans le fichier `docker-compose.yml`. Vous pouvez démarrer l'environnement avec `docker compose up -d` et l'arrêter avec `docker compose down`.

Si vous modifiez le fichier `docker-compose.yml`, vous pouvez redémarrer les conteneurs avec la commande `docker compose up -d --force-recreate`.

---

## Starting
```bash
docker ps -a
```

### Résultat / Erreur
```bash
CONTAINER ID   IMAGE         COMMAND                  CREATED       STATUS                         PORTS                                       NAMES
98e1b8d4a341   postgres:16   "docker-entrypoint.s…"   2 years ago   Restarting (1) 2 seconds ago                                               postgres-db-replica
e3810a53aa68   postgres:16   "docker-entrypoint.s…"   2 years ago   Up About a minute (healthy)    0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres-db-master
```

## Diagnostic
```bash
docker compose logs
```

### Résultat / Erreur
```bash
FATAL: recovery aborted because of insufficient parameter settings
DETAIL: max_connections = 80 is a lower setting than on the primary server, where its value was 100.
DETAIL:  max_worker_processes = 4 is a lower setting than on the primary server, where its value was 8.
DETAIL:  max_wal_senders = 5 is a lower setting than on the primary server, where its value was 10.
DETAIL:  max_locks_per_transaction = 32 is a lower setting than on the primary server, where its value was 64.
```

## Solution
```bash
cd postgres/replica/
nano postgres.conf
```

### Change

```bash
max_connections = 80
max_worker_processes = 4
max_wal_senders = 5
max_locks_per_transaction = 32
```

### By

```bash
max_connections = 100
max_worker_processes = 8
max_wal_senders = 10
#max_locks_per_transaction = 64
```

## Finalization
```bash
postgres-db-replica  | rm: cannot remove '/var/lib/postgresql/data/': Device or resource busy
postgres-db-replica  | waiting for checkpoint
postgres-db-replica  | 30153/30732 kB (98%), 0/1 tablespace
postgres-db-replica  | 30743/30743 kB (100%), 0/1 tablespace
postgres-db-replica  | 30743/30743 kB (100%), 1/1 tablespace
postgres-db-replica  | Backup done, starting replica...
postgres-db-replica  | 2026-07-17 21:15:55.008 GMT [1] LOG:  starting PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
postgres-db-replica  | 2026-07-17 21:15:55.010 GMT [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
postgres-db-replica  | 2026-07-17 21:15:55.010 GMT [1] LOG:  listening on IPv6 address "::", port 5432
postgres-db-replica  | 2026-07-17 21:15:55.017 GMT [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
postgres-db-replica  | 2026-07-17 21:15:55.026 GMT [13] LOG:  database system was interrupted; last known up at 2026-07-17 21:15:53 GMT
postgres-db-replica  | 2026-07-17 21:15:55.044 GMT [13] LOG:  entering standby mode
postgres-db-replica  | 2026-07-17 21:15:55.045 GMT [13] LOG:  starting backup recovery with redo LSN 0/56000028, checkpoint LSN 0/56000060, on timeline ID 1
postgres-db-replica  | 2026-07-17 21:15:55.052 GMT [13] LOG:  redo starts at 0/56000028
postgres-db-replica  | 2026-07-17 21:15:55.055 GMT [13] LOG:  completed backup recovery with redo LSN 0/56000028 and end LSN 0/56000100
postgres-db-replica  | 2026-07-17 21:15:55.055 GMT [13] LOG:  consistent recovery state reached at 0/56000100
postgres-db-replica  | 2026-07-17 21:15:55.055 GMT [1] LOG:  database system is ready to accept read-only connections
postgres-db-replica  | 2026-07-17 21:15:55.069 GMT [14] LOG:  started streaming WAL from primary at 0/57000000 on timeline 1

```

## Explanation
> En réplication physique PostgreSQL, la réplique rejoue le WAL (Write-Ahead Log) du primaire. Certains paramètres qui dimensionnent des structures partagées en mémoire (verrous, workers, connexions, wal senders) doivent être identiques ou supérieurs sur la réplique, car ils doivent pouvoir accueillir tout ce qui a été alloué sur le primaire au moment où le WAL a été généré. Si la réplique a des valeurs plus basses, PostgreSQL refuse de démarrer par sécurité plutôt que de risquer une réplication corrompue ou incomplète. La solution est simplement d'aligner (ou dépasser) ces paramètres sur ceux du primaire dans le postgresql.conf de la réplique, puis de relancer le conteneur.