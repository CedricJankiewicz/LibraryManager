# Projet POO
## Rendu Semaine 1

## formation du groupe
- Cédric Jankiewicz
- Loïc Roux
- Samuel Theytaz
- Thierry Perroud

## Lier une base de données locale en Programmation Orientée Objet (POO) (Python)

### Etapes principales

#### Utiliser SQLite comme moteur local
SQLite est directement intégré à Python via le module `sqlite3`.
Les données sont enregistrées dans un simple fichier local (`.db`).

#### Créer une classe pour gérer la base
Cette classe s’occupe d’ouvrir la connexion et de l’exécuter les requêtes SQL (`INSERT`, `SELECT`, `UPDATE`, `DELETE`).
Elle contient aussi une méthode pour fermer proprement la connexion à la fin du programme.

#### Créer les classes représentant les entités
Chaque table de la base devient une classe (PublishingHouse, Book, Employee, Customer, Author).
Les attributs de la classe correspondent aux colonnes de la table.
Les méthodes permettent d’ajouter, modifier, supprimer ou lire des données dans la base.

#### Utiliser les classes dans le programme principal
- Ouvrir la connexion à la base.
- Créer des objets à partir des classes et les enregistrer dans la base.
- Consulter ou modifier les données via ces objets.
- Fermer la connexion avant de quitter le programme

## MCD / MLD
![img.png](img.png)
![img_1.png](img_1.png)

## Repôt Git
https://github.com/CedricJankiewicz/LibraryManager