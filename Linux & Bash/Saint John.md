# "Saint John": what is writing to this log file?

**Date** : 16/08/2026
**Difficulté** : Facile

## TL;DR
Un script Python de test (/home/admin/badlog.py) écrivait en continu dans /var/log/bad.log ; l'identification de son PID via ps et son arrêt direct avec kill a résolu le problème.

---

## Description
Un développeur a créé un programme de test qui écrit en continu dans le fichier journal `/var/log/bad.log` et sature l'espace disque. Vous pouvez le vérifier, par exemple, avec la commande `tail -f /var/log/bad.log`.
Ce programme n'est plus nécessaire. Identifiez-le et arrêtez-le. Ne supprimez pas le fichier journal.

---

## Starting

Vérifier le contenu du log et voir l'écriture en temps réel

```bash
tail -f /var/log/bad.log
```

## Diagnostic

Rechercher le processus écrivant dans le système (filtré sur python)

```bash
ps aux | grep python
```
### Résultat / Erreur
```bash
admin        600  0.0  1.7  12508  8296 ?        S    18:43   0:00 /usr/bin/python3 /home/admin/badlog.py
root         613  0.0  3.7  26612 17376 ?        Ss   18:43   0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
admin        933  0.0  4.1  98188 19236 pts/0    Sl+  18:44   0:00 /usr/bin/python3 /usr/bin/asciinema rec -t /i-03b509cf390f9ffad -q -i 2 /var/log/cast/i-03b509cf390f9ffad
admin       1054  0.0  1.7  12840  8068 pts/1    T    18:45   0:00 python3 -v
admin       1141  0.0  0.1   5264   700 pts/1    R+   18:48   0:00 grep python
```

## Solution

Arrêter le processus responsable (PID 600)

```bash
kill -9 600
```

## Explanation
> Le problème venait d'un script Python exécuté en arrière-plan (`/home/admin/badlog.py`) sous l'identifiant de processus (PID) **600**.
> Pour résoudre ce type d'incident :
> 1. **ps aux** permet de lister tous les processus en cours d'exécution sur le système. Filtrer avec **grep python** isole rapidement les scripts Python actifs.
> 2. La commande **kill -9 600** envoie le signal **SIGKILL** au processus, forçant son arrêt immédiat sans lui laisser le temps de continuer à remplir le disque.