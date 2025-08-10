# Documentation API – SoftDesk Support

Cette documentation décrit les endpoints principaux, l’authentification, les modèles de données, et donne des exemples concrets.

## Base
- Base URL: http://localhost:8000/
- Toutes les routes d’API sont sous: `/api/`

## Authentification
  - Obtenir un token: POST `/api/token/`
    - body (JSON): 
      { "username": "à compléter", 
        "password": "à compléter" }
    - réponse: { "access": "...", "refresh": "..." }
  - Rafraîchir: POST `/api/token/refresh/`
    - body (JSON): { "refresh": "..." }
    - réponse: { "access": "..." }
  - Authorization: CHoisir l'authentification type :`Bearer <ACCESS_TOKEN>`
    - coller le token reçu

## Modèles & champs

### User
- Champs obligatoires : username, password , birth_date, first_name, last_name
- Contraintes
  - birth_date: >= 15 ans 
  - Accès: chacun ne peut lire/éditer que son propre profil (sauf admin)

### Project
- Champs obligatoires : name, description, type (back-end/front-end/iOS/Android)
- Règles
  - À la création, l’auteur est automatiquement ajouté aux contributeurs
  - Suppression logique: is_deleted=True afin de garder une trace des anciens projets

### Issue
- Champs obligatoires : title, description, tag (bug/tâche/amélioration), priority (faible/moyenne/élevée), status (à faire/en cours/terminé)
- Règles
  - L’assignee ne peut être qu'un ou plusieurs des contributeurs du projet
  - Filtrage par projet via query param `?project=<project_id>`

### Comment
- Champs obligatoires : description
- Règles
  - Filtrage par issue via query param `?issue=<issue_id>`

## Endpoints

### Users
- GET `/api/users/` (admin)
- POST `/api/users/` (inscription)
- GET `/api/users/{id}/` (propriétaire ou admin)
- PATCH `/api/users/{id}/` (propriétaire ou admin)
- DELETE `/api/users/{id}/` (propriétaire ou admin)

Exemple – inscription
```
POST /api/users/

{
  "username": "pierre",
  "password": "pierre",
  "email": "pierre@example.com",
  "first_name": "pierre",
  "last_name": "hugo",
  "birth_date": "2000-01-01",
  "can_be_contacted": false,
  "can_data_be_shared": false
}
```

### Projects
- GET `/api/projects/` (contributeurs/auteur)
- POST `/api/projects/` (user)
- GET `/api/projects/{id}/` (user)
- PATCH `/api/projects/{id}/` (auteur)
- DELETE `/api/projects/{id}/` (auteur) – soft delete

Exemple – création projet
```
POST /api/projects/
Authorization: Bearer <token> - mettre le token récupéré 

{
  "name": "Mon projet",
  "description": "Description",
  "type": "back-end",
  "contributors": [2,3]
}
```

### Issues
- GET `/api/issues/?project={project_id}` (contributeurs/auteur)
- POST `/api/issues/?project={project_id}` (contributeurs/auteur)
- GET `/api/issues/{id}/` (contributeurs/auteur)
- PATCH `/api/issues/{id}/` (auteur)
- DELETE `/api/issues/{id}/` (auteur)

Exemple – création issue
```
POST /api/issues/?project=1

{
  "title": "Problème sur projet 1",
  "description": "description",
  "tag": "bug",
  "priority": "moyenne",
  "status": "à faire",
  "assignee": 3
}
```

### Comments
- GET `/api/comments/?issue={issue_id}` (contributeurs/auteur)
- POST `/api/comments/?issue={issue_id}` (contributeurs/auteur)
- GET `/api/comments/{id}/` (contributeurs/auteur)
- PATCH `/api/comments/{id}/` (auteur)
- DELETE `/api/comments/{id}/` (auteur)

Exemple – création commentaire
```
POST /api/comments/?issue=10

{
  "description": "Je prends cette issue."
}
```
