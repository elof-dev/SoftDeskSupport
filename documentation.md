# Documentation API SoftDesk

## 1. Création d’un utilisateur (Inscription)

- **URL** : `/api/users/`
- **Méthode** : `POST`
- **Authentification requise** : Non

### Champs obligatoires

| Champ               | Type    | Exemple              | Description                                 |
|---------------------|---------|----------------------|---------------------------------------------|
| username            | string  | "elodie"             | Nom d’utilisateur unique                    |
| password            | string  | "motdepassefort"     | Mot de passe                                |
| email               | string  | "elodie@mail.com"    | Adresse email                               |
| first_name          | string  | "Elodie"             | Prénom                                      |
| last_name           | string  | "Fourcade"           | Nom                                         |
| birth_date          | date    | "2000-01-01"         | Date de naissance (format YYYY-MM-DD)       |

### Champs optionnels

| Champ               | Type    | Exemple   | Description                                 |
|---------------------|---------|-----------|---------------------------------------------|
| can_be_contacted    | bool    | true      | Peut être contacté par SoftDesk             |
| can_data_be_shared  | bool    | false     | Consentement pour partager ses données      |

### Exemple de requête

```json
POST /api/users/
{
  "username": "elodie",
  "password": "motdepassefort",
  "email": "elodie@mail.com",
  "first_name": "Elodie",
  "last_name": "Fourcade",
  "birth_date": "2000-01-01",
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

### Exemple de réponse

```json
{
  "id": 1,
  "username": "elodie",
  "email": "elodie@mail.com",
  "first_name": "Elodie",
  "last_name": "Fourcade",
  "birth_date": "2000-01-01",
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

---

## 2. Connexion (Obtenir un token JWT)

- **URL** : `/api/token/`
- **Méthode** : `POST`
- **Authentification requise** : Non

### Champs obligatoires

| Champ     | Type   | Exemple      | Description                |
|-----------|--------|--------------|----------------------------|
| username  | string | "elodie"     | Nom d’utilisateur          |
| password  | string | "motdepasse" | Mot de passe               |

### Exemple de requête

```json
POST /api/token/
{
  "username": "elodie",
  "password": "motdepassefort"
}
```

### Exemple de réponse

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Utilisez le token `access` dans l’en-tête Authorization pour toutes les requêtes protégées :**

elodie
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NTIyOTM5MSwiaWF0IjoxNzU0NjI0NTkxLCJqdGkiOiJiMmVkZjEyZjJhMTQ0MzIxOTY0Y2M1MDM1YmY1ZmZhYiIsInVzZXJfaWQiOiIyIn0.vb2utWCI6ra3W50ATwc6GC6UKsU2g_Pb1AC77NTkhFk",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0NjUzMzkxLCJpYXQiOjE3NTQ2MjQ1OTEsImp0aSI6ImFkZDM1Yjk4ODIzNTQ4ZjViZTZmNDcwY2UwNDU2ZjA3IiwidXNlcl9pZCI6IjIifQ.leCWlsWlmZmEtzGD-kh5C9XnIT2_jwx415CmUrvMR_U"
}

Création de projetcs

{
  "name": "Projet Test",
  "description": "Un projet d'exemple",
  "type": "iOS",
  "contributors": [2, 3]
}

thomas
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NTIzMjA4NywiaWF0IjoxNzU0NjI3Mjg3LCJqdGkiOiI2YWIyZGM1MDA3Njg0NzIzYTUzNjNiZDk5MTAxODczNSIsInVzZXJfaWQiOiIzIn0.3jiRoZm_YYkLf_kDlCG9Xw8r3MnHFzflK7aJuduaGng",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0NjU2MDg3LCJpYXQiOjE3NTQ2MjcyODcsImp0aSI6IjRmYjA2ZGI0YmQ4ODQwZjNiYTdhZWQ5YmI1OGIwMzhjIiwidXNlcl9pZCI6IjMifQ.mJkTd9QP6aAJK0IgGMT9SteDPTCKgHAaErgLAwBK_ow"
}

créer une issue
Pour créer une issue via l’API, tu dois faire un POST sur l’endpoint /api/issues/ (ou /api/issues/?project=<id_du_projet> si tu utilises le paramètre de projet dans l’URL).

Exemple de requête POST
URL :
http://127.0.0.1:8000/api/issues/?project=<id_du_projet>

(remplace <id_du_projet> par l’ID du projet concerné)

Headers :

Authorization: Bearer <ton_access_token>
Content-Type: application/json
Body (JSON) :
{
  "title": "Titre de l'issue",
  "description": "Description détaillée du problème",
  "tag": "bug",         
  "priority": "faible", 
  "status": "à faire", 
  "assignee": 2           // ID d'un utilisateur contributeur du projet
}