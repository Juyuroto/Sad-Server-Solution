# "Bata": Find in /proc

**Date** : 01/09/2026
**Difficulté** : facile

## TL;DR
Recherche récursive dans `/proc/sys` avec `grep` en masquant les erreurs de permission (`2>/dev/null`) pour isoler le secret (`excalibur`), puis écriture dans `/home/admin/secret.txt`.

---

## Description
Un espion a laissé un mot de passe dans un fichier dans /proc/sys. Le contenu du fichier commence par « secret : » (sans guillemets). Trouvez le fichier et enregistrez le mot après « secret : » dans le fichier /home/admin/secret.txt avec une nouvelle ligne à la fin (par exemple, si le contenu du fichier était « secret :password », faites : `echo "password" > /home/admin/secret.txt`).
(Notez qu'il n'y a pas d'accès root/sudo dans ce scénario).c

---

## Starting
```bash
cd /proc/sys
```

## Diagnostic
```bash
ls -la
```

### Résultat / Erreur
```bash
total 0
dr-xr-xr-x   1 root root 0 Sep  1 14:31 .
dr-xr-xr-x 144 root root 0 Sep  1 14:31 ..
dr-xr-xr-x   1 root root 0 Sep  1 14:32 abi
dr-xr-xr-x   1 root root 0 Sep  1 14:32 crypto
dr-xr-xr-x   1 root root 0 Sep  1 14:32 debug
dr-xr-xr-x   1 root root 0 Sep  1 14:32 dev
dr-xr-xr-x   1 root root 0 Sep  1 14:31 fs
dr-xr-xr-x   1 root root 0 Sep  1 14:31 kernel
dr-xr-xr-x   1 root root 0 Sep  1 14:32 net
dr-xr-xr-x   1 root root 0 Sep  1 14:32 user
dr-xr-xr-x   1 root root 0 Sep  1 14:32 vm
```

## Test
```bash
grep -RniI -E 'secret' /proc/sys 2>/dev/null
```

## Résultat
```bash
/proc/sys/kernel/core_pattern:1:secret:excalibur
```

## Solution
```bash
echo "excalibur" > /home/admin/secret.txt
cat /home/admin/secret.txt
```

## Explanation
> Le répertoire /proc est un système de fichiers virtuel généré dynamiquement par le noyau Linux. Sans les privilèges root, explorer cette arborescence génère beaucoup de refus d'accès : la redirection 2>/dev/null permet d'ignorer ces erreurs pour ne conserver que les résultats pertinents. Le mot de passe était caché dans /proc/sys/kernel/core_pattern sous la forme secret:excalibur. La résolution consistait à extraire le mot excalibur et à le sauvegarder avec une nouvelle ligne dans /home/admin/secret.txt.