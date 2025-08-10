# SoftDesk Support – Backend API

## Démarrage rapide

1. Installer les dépendances (Poetry)
2. Lancer le serveur Django
3. Ouvrir http://localhost:8000/

## Authentification

- JWT via `/api/token/` et `/api/token/refresh/` (voir doc API)

## Documentation API

- Voir `docs/API.md` pour les endpoints, exemples de requêtes, règles de permissions et erreurs courantes.

## Sécurité (à prévoir en production)

- Externaliser SECRET_KEY, mettre DEBUG=False, définir ALLOWED_HOSTS
- Activer HTTPS/HSTS et cookies sécurisés
- Ajouter pagination et throttling dans DRF
