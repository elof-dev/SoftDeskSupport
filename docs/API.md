# Documentation API – SoftDesk Support

Cette documentation décrit les endpoints principaux, l’authentification, les modèles de données, et donne des exemples concrets.

## Base
- Base URL (dev): http://localhost:8000/
- Toutes les routes d’API sont sous: `/api/`
- Redirection: `/` -> `/api/`

## Authentification
- JWT (JSON Web Token)
  - Obtenir un token: POST `/api/token/`
    - body (JSON): { "username": "alice", "password": "***" }
    - réponse: { "access": "...", "refresh": "..." }
  - Rafraîchir: POST `/api/token/refresh/`
    - body (JSON): { "refresh": "..." }
    - réponse: { "access": "..." }
- Headers requis
  - Authorization: `Bearer <ACCESS_TOKEN>`

## Modèles & champs

### User
- Champs: id, username, password (write-only), email, birth_date, can_be_contacted, can_data_be_shared, first_name, last_name
- Contraintes
  - birth_date: >= 15 ans (sinon 400)
  - Accès: chacun ne peut lire/éditer que son propre profil (sauf admin)

### Project
- Champs: id, name, description, type (back-end/front-end/iOS/Android), author (read-only username), contributors [user ids], created_time
- Règles
  - À la création, l’auteur est automatiquement ajouté aux contributeurs
  - Suppression logique: is_deleted=True

### Issue
- Champs: id, title, description, tag (bug/tâche/amélioration), priority (faible/moyenne/élevée), status (à faire/en cours/terminé), project (read-only), author, assignee, created_time, updated_time
- Règles
  - L’assignee doit être contributeur du projet (ou l’auteur)
  - Filtrage par projet via query param `?project=<project_id>`

### Comment
- Champs: id, issue (read-only), author (read-only username), description, created_time, updated_time
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
Content-Type: application/json

{
  "username": "alice",
  "password": "S3cret!",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Doe",
  "birth_date": "2000-01-01",
  "can_be_contacted": false,
  "can_data_be_shared": false
}
```

### Projects
- GET `/api/projects/` (contributeurs/auteur)
- POST `/api/projects/`
- GET `/api/projects/{id}/`
- PATCH `/api/projects/{id}/` (auteur)
- DELETE `/api/projects/{id}/` (auteur) – soft delete

Exemple – création projet
```
POST /api/projects/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Mon projet",
  "description": "Description",
  "type": "back-end",
  "contributors": [2,3]
}
```

### Issues
- GET `/api/issues/?project={project_id}` (contributeurs/auteur)
- POST `/api/issues/?project={project_id}`
- GET `/api/issues/{id}/`
- PATCH `/api/issues/{id}/` (auteur)
- DELETE `/api/issues/{id}/` (auteur)

Exemple – création issue
```
POST /api/issues/?project=1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Bug page login",
  "description": "Repro...",
  "tag": "bug",
  "priority": "moyenne",
  "status": "à faire",
  "assignee": 3
}
```

### Comments
- GET `/api/comments/?issue={issue_id}` (contributeurs/auteur)
- POST `/api/comments/?issue={issue_id}`
- GET `/api/comments/{id}/`
- PATCH `/api/comments/{id}/` (auteur)
- DELETE `/api/comments/{id}/` (auteur)

Exemple – création commentaire
```
POST /api/comments/?issue=10
Authorization: Bearer <token>
Content-Type: application/json

{
  "description": "Je prends cette issue."
}
```

## Sécurité et permissions
- Auth: JWT obligatoire (sauf POST /api/users/ pour inscription)
- Permissions
  - Par défaut: IsAuthenticated
  - Users: IsSelfOrAdmin
  - Projects/Issues/Comments: 
    - List/Read: contributeur/auteur du projet
    - Create: contributeur du projet (via param parent)
    - Update/Delete: auteur uniquement

## Erreurs courantes
- 401 Unauthorized: token manquant/expiré
- 403 Forbidden: pas contributeur/pas auteur
- 400 Bad Request: validation (âge < 15 ans, assignee hors contributeurs)
- 404 Not Found: project/issue inexistant ou soft-deleted

## Bonnes pratiques d’usage
- Toujours passer `Authorization: Bearer <access>`
- Utiliser les query params parent: `?project=` pour Issues, `?issue=` pour Comments
- Rafraîchir l’access token via `/api/token/refresh/` avant expiration

## Notes (implémentation actuelle)
- Pagination non configurée – à ajouter si volumétrie élevée
- Throttling non configuré – à ajouter pour limiter le brute-force / abus
- En prod: externaliser SECRET_KEY, mettre DEBUG=False, définir ALLOWED_HOSTS, activer HTTPS/HSTS/cookies sécurisés
