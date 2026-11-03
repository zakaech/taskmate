# Cahier des charges : TaskMate

## 1. Présentation
TaskMate est une application web de gestion de tâches (to-do list) permettant d'organiser son travail par catégorie, priorité et date limite.

## 2. Exigences fonctionnelles

| ID | Exigence |
|----|----------|
| EF1 | L'utilisateur peut créer une tâche (titre, catégorie, priorité, date limite) |
| EF2 | L'utilisateur peut modifier une tâche |
| EF3 | L'utilisateur peut supprimer une tâche |
| EF4 | L'utilisateur peut marquer une tâche comme terminée |
| EF5 | L'utilisateur peut filtrer les tâches par catégorie, priorité et statut |
| EF6 | L'utilisateur peut trier les tâches par date limite |
| EF7 | L'utilisateur peut voir des statistiques (total, terminées, restantes) |

## 3. Exigences non fonctionnelles

| ID | Exigence |
|----|----------|
| ENF1 | Le titre est obligatoire ; la priorité est `low`, `medium` ou `high` ; la date est au format AAAA-MM-JJ |
| ENF2 | Les données sont conservées dans une base SQLite |
| ENF3 | L'architecture est en couches (routes / service / repository) |
| ENF4 | Le code est couvert par des tests automatisés exécutés à chaque Pull Request |
| ENF5 | L'application s'installe et se lance en moins de 5 commandes |

## 4. Acteur
- **Utilisateur** : toute personne qui gère ses tâches.

## 5. Cas d'utilisation
Créer une tâche, modifier une tâche, supprimer une tâche, terminer une tâche, filtrer, trier, consulter les statistiques.

## 6. Contraintes
Python 3 / Flask, SQLite, HTML/CSS/JS sans framework, GitHub pour le versionnement.