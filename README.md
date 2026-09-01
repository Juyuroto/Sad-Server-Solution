# Sad-Server-Solution

Ce dépôt regroupe l'ensemble de mes solutions et write-ups pour les scénarios du site [SadServers](https://sadservers.com/). Chaque fichier détaille le diagnostic, la résolution étape par étape ainsi que les explications techniques pour résoudre les pannes d'infrastructure, de bases de données, de conteneurs et de sécurité Linux.

---

## Liste des Scénarios

### Database
| Scénario | Description | Fichier |
| :--- | :--- | :--- |
| **Bucharest** | Résolution de problèmes de réplication PostgreSQL et ajustement des paramètres du fichier de configuration (`postgres.conf`). | [`Bucharest.md`](./Database/Bucharest.md) |

---

### Docker
| Scénario | Description | Fichier |
| :--- | :--- | :--- |
| **Bharuch** | Résolution d'un conflit d'architecture CPU (**arm64** vs **amd64**) provoquant l'erreur `exec format error`. | [`Bharuch.md`](./Docker/Bharuch.md) |
| **Helsingør** | Correction d'une boucle de redémarrage sur une réplique PostgreSQL due à une sous-configuration dans `postgres.conf`. | [`Helsingør.md`](./Docker/Helsingør.md) |
| **Podgorica** | Migration vers Podman rootless et automatisation du conteneur via un service systemd utilisateur (linger). | [`Podgorica.md`](./Docker/Podgorica.md) |
| **Quito** | Prise de contrôle du daemon Docker de l'hôte depuis un conteneur via le montage de `/var/run/docker.sock`. (`docker.sock`). | [`Quito.md`](./Docker/Quito.md) |
| **Salta** | Résolution d'un conflit de port (8888 occupé par Nginx) et correction d'erreurs dans le **Dockerfile** Node.js. | [`Salta.md`](./Docker/Salta.md) |
| **Tarifa** | Debugging d'un load balancer HAProxy avec Docker Compose (correction des réseaux et conflits de ports Nginx). | [`Tarifa.md`](./Docker/Tarifa.md) |
| **Venice** | Identification de l'environnement d'exécution (détection de virtualisation KVM vs conteneurisation). | [`Venice.md`](./Docker/Venice.md) |
| **Woluwe** | Identification de l'image Docker sans faute de frappe via **docker history**, tag en **prod** et nettoyage des autres images. | [`Woluwe.md`](./Docker/Woluwe.md) |

---

### Hacking
| Scénario | Description | Fichier |
| :--- | :--- | :--- |
| **Madrid** | Analyse de logs de sécurité et détection d'intrusions / attaques. | [`Madrid.md`](./Hacking/Madrid.md) |
| **Monaco** | Identification et colmatage de vulnérabilités système et d'élévation de privilèges. | [`Monaco.md`](./Hacking/Monaco.md) |
| **Roseau** | Investigation médico-légale (*forensics*) suite à un compromis système. | [`Roseau.md`](./Hacking/Roseau.md) |

---

### Linux & Bash
| Scénario | Description | Fichier |
| :--- | :--- | :--- |
| **Saint John** | Résolution de problèmes d'E/S disque, d'espace plein ou de processus zombies. | [`Saint John.md`](./Linux%20%26%20Bash/Saint%20John.md) |
| **Saskatoon** | Écriture de scripts Bash pour l'automatisation de maintenance système. | [`Saskatoon.md`](./Linux%20%26%20Bash/Saskatoon.md) |

---

## Structure des Scénarios
Chaque scénario suit le template officiel défini dans [`template.md`](./template.md) :
1. **Description / TL;DR** : Résumé de la panne et de la solution.
2. **Starting** : État initial du serveur.
3. **Diagnostic** : Commandes et logs d'analyse pour trouver l'origine du problème.
4. **Solution** : Corrections apportées pas à pas.
5. **Finalization & Explanation** : Vérification de la résolution et explication théorique.