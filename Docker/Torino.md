# "Torino": Optimize grande Docker image

**Date** : 02/09/2026
**Difficulté** : moyen

## TL;DR
Optimiser une image node pour passer de 916 Mo à 122 Mo, en utilisant une autre image node:16 à node:16-alpine. Il va falloir modifier le Dockerfile à la racine du folder ~/torino-app

---

## Description
Une application Torino Node.js se trouve dans le répertoire ~/torino-app. 
Vous pouvez l'exécuter directement avec : `nohup node app.js > app.log 2>&1 &`. Vous pouvez aussi vérifier que ça fonctionne en exécutant : `curl localhost:3000`
Il existe déjà une image Docker Torino construite avec le fichier Docker dans ~/torino-app, mais la taille d'image résultante est de 916 Mo. 
Votre tâche est d'optimiser la taille de l'image Docker : 
1. Créer une nouvelle image Docker pour l'application Torino, également appelée torino :latest mais avec une taille totale inférieure à 122 Mo 
2. Créer et exécuter un conteneur en utilisant cette image optimisée. 

REMARQUE : Vous ne pouvez utiliser que les images Docker existantes sur le serveur. 
Pour construire une application Node, il faut COPIER dans votre fichier Dockerfile, en plus du app.js, du package*.json et sans accès Internet, le répertoire node_modules, car vous ne pouvez pas LANCER l'installation de npm.

---

## Starting
```bash
cd torino-app
cat Dockerfile
docker images
```

## Résultat
```bash
# Dockerfile
FROM node:16

WORKDIR /app

COPY package.json .
COPY app.js .

RUN npm install

EXPOSE 3000

CMD ["node", "app.js"]

# Docker Images
REPOSITORY   TAG         IMAGE ID       CREATED        SIZE
torino       latest      79ab8632f03a   8 months ago   916MB
node         16          1ddc7e4055fd   2 years ago    909MB
node         16-alpine   2573171e0124   3 years ago    118MB
```

## Diagnostic
```bash
curl localhost:3000
```

## Résultat / Erreur
```bash
curl: (7) Failed to connect to localhost port 3000 after 0 ms: Could not connect to server
```

## Change
```bash
FROM node:16

WORKDIR /app

COPY package.json .
COPY app.js .

RUN npm install

EXPOSE 3000

CMD ["node", "app.js"]
```

## Par
```bash
FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --production && \
    npm cache clean --force && \
    rm -rf /tmp/* /var/cache/apk/*

COPY app.js ./

EXPOSE 3000

CMD ["node", "app.js"]
```

### Test
```bash
docker build -t torino .
docker run -d --name torino -p 3000:3000 torino
curl localhost:3000
```

## Résultat / Erreur
```bash
{"message":"Hello from Torino!"}
```

## Explanation
> Sur le serveur, on avait à disposition plusieurs images comme torino:latest, node:16-alpine et node:16, avec un poid au dessus de 916 Mo, sauf une. node:16-alpine est une image légère de nodejs, donc on pouvait modifier le Dockerfile pour choisir cette image.