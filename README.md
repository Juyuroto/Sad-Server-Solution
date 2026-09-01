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
| **Bharuch** | Diagnostic et correction de conteneurs Docker défaillants ou mal configurés. | [`Bharuch.md`](./Docker/Bharuch.md) |
| **Helsingør** | Résolution de conflits de ports et de communication réseau entre conteneurs. | [`Helsingør.md`](./Docker/Helsingør.md) |
| **Quito** | Prise de contrôle d'un conteneur à partir d'un autre via le partage du socket Docker (`docker.sock`). | [`Quito.md`](./Docker/Quito.md) |
| **Salta** | Correction des volumes et de la persistance de données sous Docker. | [`Salta.md`](./Docker/Salta.md) |
| **Tarifa** | Debugging d'images Docker et gestion des dépendances système en erreur. | [`Tarifa.md`](./Docker/Tarifa.md) |
| **Venice** | Optimisation des dépendances et réparation des services multi-conteneurs. | [`Venice.md`](./Docker/Venice.md) |

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