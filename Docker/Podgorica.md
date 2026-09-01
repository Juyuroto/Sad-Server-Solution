# "Podgorica": Docker to Podman migration

**Date** : 01/09/2026
**Difficulté** : moyen

## TL;DR
Génération d'un service utilisateur systemd via `podman generate systemd --new` pour gérer un conteneur Nginx rootless, suivi de l'activation du *linger* avec `loginctl` pour garantir le démarrage au boot sans session active.

---

## Description
Vous avez pour mission de migrer ce futur serveur web de l'utilisation de Docker (qui utilise un daemon) vers **rootless Podman**. Il existe déjà une image Nginx Podman sur le serveur, et votre objectif est de gérer le conteneur créé à partir de celle-ci via systemd, afin qu'il démarre automatiquement au redémarrage et continue de fonctionner sauf s'il est explicitement arrêté (le même comportement attendu d'un conteneur géré par Docker). Créez un service systemd nommé container-nginx.service qui gère le conteneur Podman Nginx. Activez et lancez ce service.

REMARQUES : Bien qu'une solution de fichier quadlet devrait être valide, le script de vérification ne l'inclut toujours pas. 

Il n'est pas nécessaire de redémarrer la VM, bien que si vous le souhaitez, vous puissiez la redémarrer depuis la ligne de commande avec `/sbin/shutdown -r now` et rafraîchir ou rouvrir la console web.

---

## Starting

### Vérification
```bash
podman -v
podman images
```

### Retour
```bash
podman version 5.4.2

REPOSITORY               TAG         IMAGE ID      CREATED       SIZE
docker.io/library/nginx  latest      576306625d79  8 months ago  156 MB
```

## Solution

### 1.Créer le répertoire des services utilisateur systemd
```bash
mkdir -p ~/.config/systemd/user
cd ~/.config/systemd/user
```

### 2.Créer le conteneur modèle
```bash
podman create \
  --name nginx \
  --publish 8888:80 \
  576306625d79
```

### 3.Générer le fichier de service systemd
```bash
podman generate systemd \
  --name nginx \
  --files \
  --new \
  --restart-policy=always
```

### 4.Nettoyer le conteneur temporaire & démarrer le service
```bash
podman rm nginx
systemctl --user daemon-reload
systemctl --user enable --now container-nginx.service
```

## 5.Permettre le démarrage automatique au boot (Linger)
```bash
loginctl enable-linger "$USER"
```

## Test / Validation
```bash
# Vérifier le statut du service systemd
systemctl --user status container-nginx.service

# Tester l'accès au serveur web
curl localhost:8888
```

## Explanation
Contrairement à Docker qui s'appuie sur un daemon centralisé tournant en `root`, Podman fonctionne en mode rootless (sans privilèges superadministrateur). Pour qu'un conteneur Podman démarre automatiquement comme un service système, on utilise `systemd` au niveau de l'utilisateur (`~/.config/systemd/user`).
Les étapes clés à retenir :
  - `podman generate systemd --new` : Génère le fichier `container-nginx.service`. L'argument `--new` signifie que systemd va créer et détruire automatiquement un nouveau conteneur à chaque démarrage/arrêt du service. C'est pourquoi il faut supprimer le conteneur temporaire (podman rm nginx) avant de lancer le service.
  - `systemctl --user` : Permet de gérer les services propres à l'utilisateur courant sans avoir besoin des droits `root`.
  - `loginctl enable-linger "$USER"` : Étape cruciale en rootless. Par défaut, les services utilisateur systemd s'arrêtent dès que l'utilisateur ferme sa session SSH. Le linger autorise le système à exécuter les services de l'utilisateur dès le démarrage de la machine, même sans session active.