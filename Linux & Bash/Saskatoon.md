# "Saskatoon": counting IPs

**Date** : 16/08/2026
**Difficulté** : facile

## TL;DR
Extraction de la première colonne (adresses IP) du fichier journal /home/admin/access.log, tri et décompte des occurrences pour isoler l'IP la plus fréquente (66.249.73.135), puis enregistrement du résultat dans /home/admin/highestip.txt.

---

## Description
Un fichier journal d'accès du serveur web se trouve à l'emplacement `/home/admin/access.log`. Ce fichier contient une ligne par requête HTTP, l'adresse IP du demandeur figurant au début de chaque ligne (première colonne).

Identifiez l'adresse IP associée au plus grand nombre de requêtes dans ce fichier (il n'y a pas d'égalité ; l'adresse IP est unique). Enregistrez la solution dans le fichier `/home/admin/highestip.txt`. Par exemple, si votre solution est « 1.2.3.4 », vous pouvez utiliser la commande `echo "1.2.3.4" > /home/admin/highestip.txt`.

REMARQUE : L'adresse IP trouvée apparaît 482 fois (c'est-à-dire que la commande `grep -c -F -f highestip.txt access.log` renvoie 482) ; si vous obtenez un nombre différent (inférieur), c'est que vous n'avez pas identifié la bonne adresse IP la plus fréquente.

---

### Inspecter le début du fichier journal pour vérifier la structure des colonnes

## Starting
```bash
head -n 5 /home/admin/access.log
```

## Diagnostic

### Extraire la 1ère colonne (IP), trier, compter les occurrences uniques, puis trier par fréquence

```bash
awk '{print $1}' /home/admin/access.log | sort | uniq -c | sort -nr | head -n 1
```

### Résultat / Erreur

```bash
482 66.249.73.135
```

### Écrire l'IP la plus fréquente directement dans le fichier cible

## Solution
```bash
echo -n "66.249.73.135" > /home/admin/highestip.txt
```

## Explanation
> Le traitement des fichiers de logs texte sous Linux repose souvent sur la combinaison de pipeline d'outils textuels classique :
> 1. `awk '{print $1}'` : Extrait le premier champ (délimité par un espace par défaut) de chaque ligne, correspondant à l'adresse IP.
> 2. **sort** : Trie les IP par ordre alphabétique. Cette étape est obligatoire avant **uniq**, car **uniq** ne regroupe que les lignes contiguës.
> 3. `uniq -c` : Déduplique les lignes identiques tout en préfixant chaque ligne par le nombre d'occurrences.
> 4. `sort -nr` : Trie le résultat numériquement (**-n**) et par ordre décroissant (**-r**) afin de placer l'IP la plus fréquente au sommet de la liste.
> 5. `head -n 1` : Isole la toute première ligne du résultat.