# "Woluwe": Too many images

**Date** : 01/09/2026
**Difficulté** : moyen

## TL;DR
Inspection de l'historique des images avec `docker history` et `grep` pour isoler l'image sans la coquille `index.htmlz`, étiquetage en `prod`, nettoyage des autres images et déploiement sur le port 3000.

---

## Description
Un pipeline a créé beaucoup d'images Docker localement pour une application web. Toutes ces images, sauf une, contiennent une faute de frappe introduite par un développeur : il y a une instruction image incorrecte pour canaliser « HelloWorld » vers « index.htmlz » au lieu d'utiliser le bon « index.html » 
Trouvez quelle image n'a pas la faute de frappe (et utilise le bon « index.html »), identifiez cette image correcte comme « prod » (plutôt que de corriger l'image prod actuelle), puis déployez-la avec `docker run -d ---name prod -p 3000:3000` prod pour qu'elle réponde correctement aux requêtes HTTP sur le port :3000 au lieu de « 404 Not Found ».

---

## Starting
```bash
docker images
```

## Resultat
```bash
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
prod         latest    7ef77e0bb072   9 months ago    5.32MB
<none>       <none>    e991a67a5388   9 months ago    5.32MB
<none>       <none>    1f73440c64c1   9 months ago    5.32MB
<none>       <none>    4181cb5d8a97   9 months ago    5.32MB
<none>       <none>    37f1b9840b69   9 months ago    5.32MB
<none>       <none>    2e3c60654bae   9 months ago    5.32MB
<none>       <none>    841990e44da7   9 months ago    5.32MB
<none>       <none>    e47fb961b1b8   9 months ago    5.32MB
<none>       <none>    0ac49b75b0ac   9 months ago    5.32MB
<none>       <none>    ad9c706df5da   9 months ago    5.32MB
<none>       <none>    6ebd212e6034   9 months ago    5.32MB
<none>       <none>    cc5260c6392e   9 months ago    5.32MB
<none>       <none>    ef28344e373e   9 months ago    5.32MB
<none>       <none>    8236dee69cea   9 months ago    5.32MB
<none>       <none>    6a2951b3311f   9 months ago    5.32MB
<none>       <none>    0ac5927ec39d   9 months ago    5.32MB
<none>       <none>    6ce8cc718ad1   9 months ago    5.32MB
<none>       <none>    52eab2232d8e   9 months ago    5.32MB
base         latest    dd15126afe8d   10 months ago   4.27MB
```

## Diagnostic
```bash
for img in $(docker images -q); do docker history --no-trunc $img | grep -q 'index.html[^z]' && echo $img; done
```

### Résultat / Erreur
```bash
3f8befa65f01
```

## Solution
```bash
docker rmi prod
docker tag 3f8befa65f01 prod
docker rmi -f $(docker images -q | grep -v $(docker images -q prod))
docker run -d --name prod -p 3000:3000 prod
```

## Test
```bash
curl localhost:3000
```

## Resultat
```bash
HelloWorld;529
```

## Explanation
> La commande docker history --no-trunc <image_id> permet d'analyser l'ensemble des couches de chaque image. L'utilisation de grep -v "index.htmlz" filtre l'image exempte d'erreur. Après l'avoir étiquetée prod, une boucle for compare l'ID de chaque image locale à $PROD_ID afin de supprimer uniquement les images obsolètes sans générer d'erreur de syntaxe. Enfin, le conteneur est déployé avec le mapping de port -p 3000:3000.