```bash
sudo services postgresql status
PGPASSWORD=app1user psql -h 127.0.0.1 -d app1 -U app1user -c '\q'
```

## Error

```bash
psql: error: FATAL:  pg_hba.conf rejects connection for host "127.0.0.1", user "app1user", database "app1", SSL on
FATAL:  pg_hba.conf rejects connection for host "127.0.0.1", user "app1user", database "app1", SSL off
```

## Solution

```bash
cd /etc/postgresql/13/main
ls
sudo nano pg.hba.conf
```

### Contained in pg.hba.conf

![Texte alternatif](./picture/pg.hba.conf.png "Le titre de mon image")

### To change

```
# Database administrative login by Unix domain socket
local     all     postgres                  peer
host      all     all           all         reject
host      all     all           all         reject
```

### For

```
# Database administrative login by Unix domain socket
local     all     postgres                      peer
#host     all     all           all             reject
#host     all     all           all             reject
host      all     app1user      127.0.0.1/32    md5
```

## Explanation

>Le fichier pg_hba.conf bloquait les connexions réseau par sécurité ; j'ai donc désactivé ces règles de rejet et autorisé spécifiquement votre utilisateur app1user à se connecter en local avec son mot de passe.