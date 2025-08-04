# Récapitulatif de la mise en place de l’API Django SoftDesk

## 1. Création et configuration du projet

- Création du projet Django et des apps `users` (pour le modèle User personnalisé) et `softdesk` (pour la logique métier).
- Ajout des apps dans `INSTALLED_APPS` dans `settings.py`.

## 2. Modèle User personnalisé

- Création d’un modèle `User` dans l’app `users`, héritant de `AbstractUser`.
- Ajout des champs personnalisés : `birth_date`, `can_be_contacted`, `can_data_be_shared`.
- Suppression du modèle `UserProfile` (devenu inutile).
- Configuration dans `settings.py` :
  ```python
  AUTH_USER_MODEL = 'users.User'
  ```

## 3. Sérialiseur et vue User

- Création d’un `UserSerializer` dans `users/serializers.py` :
  - Champs obligatoires : `first_name`, `last_name`, `birth_date`.
  - Validation de l’âge minimum (15 ans) via `validate_birth_date`.
- Création d’un `UserViewSet` dans `users/views.py` :
  - Permissions : 
    - Création ouverte (`AllowAny`)
    - Modification/suppression réservée à l’utilisateur lui-même ou à un admin (`IsSelfOrAdmin`)
    - Lecture réservée aux utilisateurs authentifiés
  - Vérification de l’âge à la création.

## 4. Authentification JWT

- Installation et configuration de `djangorestframework-simplejwt`.
- Ajout dans `settings.py` :
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework_simplejwt.authentication.JWTAuthentication',
      ),
      'DEFAULT_PERMISSION_CLASSES': (
          'rest_framework.permissions.IsAuthenticated',
      ),
  }
  ```
- Ajout des routes JWT dans `config/urls.py` :
  ```python
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  ```

## 5. Modèles métier (softdesk)

- Création des modèles `Project`, `Contributor`, `Issue`, `Comment` dans `softdesk/models.py`.
- `Contributor` : table de liaison entre `User` et `Project`.
- Lors de la création d’un projet, ajout automatique de l’auteur comme contributor avec le rôle "author".

## 6. Sérialiseurs et vues métier

- Création des serializers et viewsets pour `Project` et `Contributor`.
- Ajout des routes dans `softdesk/urls.py` et inclusion dans `config/urls.py`.

## 7. Admin Django

- Enregistrement du modèle `User` dans `users/admin.py` pour voir les utilisateurs dans l’admin.
- Enregistrement des modèles métier dans `softdesk/admin.py`.

## 8. Migrations

- Suppression des anciennes migrations et de la base de données lors de changements majeurs sur le modèle User.
- Recréation des migrations et de la base avec :
  ```
  poetry run python manage.py makemigrations
  poetry run python manage.py migrate
  ```

## 9. Tests et utilisation de Postman

- Obtention d’un token JWT via `/api/token/` (POST avec username et password).
- Utilisation du token `access` dans Postman (onglet Authorization > Bearer Token).
- Vérification de l’en-tête Authorization dans les requêtes.
- Utilisation de PATCH pour modifier partiellement un utilisateur.
- Résolution des erreurs courantes :
  - 403 Forbidden : souvent dû à l’absence ou l’expiration du token.
  - "Token is expired" : régénérer un token via `/api/token/` ou `/api/token/refresh/`.

## 10. Points de vigilance et bonnes pratiques

- Toujours utiliser `create_user` pour créer un utilisateur (mot de passe hashé).
- Ne jamais modifier `AUTH_USER_MODEL` pour pointer vers autre chose que le modèle principal User.
- Les validations spécifiques à l’API sont à mettre dans le serializer, les validations globales dans le modèle.
- Pour chaque modification majeure du modèle User, repartir sur une base propre si possible.

---

## Problèmes rencontrés et solutions

- **InconsistentMigrationHistory** : résolu en supprimant toutes les migrations et la base, puis en recréant.
- **403 Forbidden** : résolu en ajoutant le token JWT dans les requêtes.
- **Token expired** : résolu en régénérant un token d’accès.
- **Champ password requis en PUT** : utiliser PATCH pour les modifications partielles.

---

## Exemple de workflow Postman

1. POST `/api/token/` avec username/password → récupérer le token `access`.
2. GET `/api/users/4/` avec Authorization : Bearer `<access_token>`.
3. PATCH `/api/users/4/` pour modifier un champ (ex : birth_date).

---

**Bravo pour la progression et la rigueur dans la mise en place de ton