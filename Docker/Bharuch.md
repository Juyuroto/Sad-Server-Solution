"Bharuch": Lost in Translation

**Date** : 17/07/2026
**Difficulté** : moyen

## TL;DR
Le conteneur `web-server` bouclait en restart avec `exec format error`. Cause : l'image Docker avait été buildée en `arm64` alors que l'hôte est en `x86_64`/`amd64`. Pas de Dockerfile disponible, code extrait directement depuis l'image puis rebuild avec `--platform linux/amd64`.

---

## Description
Un conteneur Docker exécute un serveur web sur le port 3000, mais il ne fonctionne pas.
À l'aide des outils et des ressources disponibles sur le serveur, faites en sorte que le conteneur fonctionne correctement.

---

## Starting
```bash
docker ps -a
```

## Result
```bash
CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS                           PORTS     NAMES
3e2e878ab10c   web-server:latest   "/bin/sh -c 'python …"   14 months ago   Restarting (255) 4 seconds ago             web-server
```

## Diagnostic
```bash
docker logs web-server
uname -m
docker image inspect web-server:latest --format '{{.Architecture}}'
docker image inspect web-server:latest --format '{{.RepoDigests}}'
```

### Result / Errorr
```bash
exec /bin/sh: exec format error

x86_64          # architecture de l'hôte
arm64           # architecture de l'image
[]              # RepoDigests vide -> image buildée localement, pas pullée
```

## Solution
```bash
docker create --name temp-extract web-server:latest
docker cp temp-extract:/app ./app-extracted
docker rm temp-extract

cd app-extracted
nano dockerfile

# In dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt 2>/dev/null || true
CMD ["python", "app.py"]
# CTRL + S & CTRL + X

docker build --platform linux/amd64 -t web-server:latest .
```

## Finalization
```bash
docker rm -f web-server
docker run -d -p 3000:3000 --name web-server web-server:latest
curl http://localhost:3000
```

## Explanation
> Le message `exec format error` ne veut pas dire que le programme a un bug logique — il veut dire que le noyau Linux est incapable de charger le binaire car il a été compilé pour un jeu d'instructions CPU différent (ici `arm64` au lieu de `x86_64`). Docker ne fait pas d'émulation d'architecture par défaut : si l'image a été buildée sur une machine ARM (typiquement un Mac Apple Silicon) sans préciser la plateforme cible, elle contient des binaires ARM inutilisables sur un serveur x86_64. Comme il n'y avait pas de Dockerfile sur le disque, la seule option était d'extraire le contenu de l'image elle-même via `docker create` + `docker cp` (ça fonctionne car l'image contient le filesystem complet, même sans pouvoir l'exécuter). Une fois le code récupéré, il suffit d'un Dockerfile minimal et d'un rebuild avec `--platform linux/amd64` pour forcer la bonne architecture. Le nom du scénario ("Lost in Translation") est un clin d'œil direct à ce problème de "traduction" entre architectures CPU.