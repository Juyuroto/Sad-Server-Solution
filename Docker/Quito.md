# "Quito": Control One Container from Another

**Date** : 01/09/2026
**Difficulté** : moyen

## TL;DR
Le conteneur **docker-access** nécessitait un montage du socket Docker hôte `/var/run/docker.sock` et un processus d'arrière-plan pour rester actif. Une fois monté et le conteneur démarré, la commande docker start nginx a été exécutée depuis l'intérieur du shell de docker-access.

---

## Description
Vous avez un conteneur en cours d'exécution nommé docker-access. Un autre conteneur, nginx, est présent mais en état arrêté. Votre objectif est de démarrer le conteneur nginx depuis l'intérieur du conteneur docker-access. 
Vous ne devez pas démarrer le conteneur nginx depuis le système hôte ni tout autre conteneur qui n'est pas docker-access. Vous pouvez redémarrer ce conteneur docker-access.

---

## Starting
```bash
docker ps -a
docker exec -it docker-access sh
```

### Résultat / Erreur
```bash
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS                      PORTS   NAMES
6d07db770d87   nginx           "/docker-entrypoint.…"   16 months ago   Exited (137) 16 months ago          nginx
1566600ac41c   docker-access   "sh"                     16 months ago   Up 5 minutes                        docker-access

Error response from daemon: container 1566600ac41c is not running
```

## Diagnostic
```bash
docker logs docker-access
```

### Résultat / Erreur
```bash
# Le conteneur docker-access n'a pas accès au socket Docker par défaut et s'arrête 
# immédiatement s'il ne possède pas de processus principal au premier plan.
tail: can't open '/dev/nul': No such file or directory
```

## Solution
```bash
docker rm -f docker-access

# 2. Redémarrage de docker-access en montant le socket Docker hôte et en maintenant le conteneur actif
docker run -d \
  --name docker-access \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docker-access tail -f /dev/null

# 3. Accès au shell du conteneur docker-access
docker exec -it docker-access sh
```

## Finalization
```bash
docker start nginx
docker ps
```

## Explanation
> Pour permettre à un conteneur de piloter le démon Docker du système hôte (pattern Docker-out-of-Docker / DooD), il est nécessaire d'exposer le Socket Unix `/var/run/docker.sock` de l'hôte à l'intérieur du conteneur cible via un volume (`-v /var/run/docker.sock:/var/run/docker.sock`).
De plus, afin d'éviter l'arrêt prématuré du conteneur docker-access lors du redémarrage, la commande tail -f /dev/null a été utilisée pour maintenir un processus d'arrière-plan actif. Une fois ces conditions réunies, l'interaction avec l'API Docker depuis le conteneur docker-access a permis de démarrer le conteneur nginx.