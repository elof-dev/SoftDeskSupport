# Audit sécurité et optimisation – SoftDesk Support

Dernière mise à jour : 2025-08-10

Source de vérité attendue : « Softdesk exigences de sécurité et d’optimisation » (PDF). Ce document compile chaque exigence, son statut de conformité (Oui / Non / Partiel), où c’est implémenté dans le code, comment cela fonctionne et comment corriger si nécessaire.

Légende statut : 
- Oui : conforme
- Non : non conforme
- Partiel : présent mais améliorable ou incomplet
- À vérifier : dépend d’un détail du PDF manquant ici

---

## Matrice de conformité (alignée sur le PDF)

| Exigence (résumé) | Statut | Références code | Explication rapide | Remédiation si Non/Partiel |
|---|:--:|---|---|---|
| [OWASP/AAA] Authentification par JWT | Oui | `config/settings.py` → REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES, SIMPLE_JWT; `config/urls.py` → `api/token/` | JWT activé pour émettre/valider access/refresh tokens. | — |
| [OWASP/AAA] Accès global réservé aux utilisateurs authentifiés | Oui | `config/settings.py` → DEFAULT_PERMISSION_CLASSES=IsAuthenticated | Par défaut, toute requête nécessite une authentification. | — |
| [OWASP/AAA] Autorisation: accès uniquement aux projets dont on est contributeur | Oui | `softdesk/views.py` → `ProjectViewSet.get_queryset`/`IssueViewSet.get_queryset`/`CommentViewSet.get_queryset`; `softdesk/permissions.py` → `IsProjectContributor` | Les listes ne renvoient que les ressources liées aux projets de l’utilisateur (auteur ou contributeur). | — |
| [OWASP/AAA] Auteur sur les ressources (projet/issue/commentaire) | Oui | `softdesk/models.py` → FK `author` sur Project/Issue/Comment | Permet d’appliquer des permissions objet (auteur seul peut modifier/supprimer). | — |
| [OWASP/AAA] Commentaires visibles par tous les contributeurs et le responsable | Oui | `CommentViewSet.get_queryset` | Filtrage par appartenance au projet du commentaire. | — |
| [OWASP/AAA] Commentaires: seul l’auteur peut mettre à jour/supprimer | Oui | `softdesk/permissions.py` → `IsAuthor`; `CommentViewSet.get_permissions` | `update/partial_update/destroy` réservés à l’auteur. | — |
| [OWASP/AAA] Issues visibles par tous les contributeurs | Oui | `IssueViewSet.get_queryset` | Filtrage par projet et contribution. | — |
| [OWASP/AAA] Issues: seul l’auteur peut mettre à jour/supprimer | Oui | `softdesk/permissions.py` → `IsAuthor`; `IssueViewSet.get_permissions` | `update/partial_update/destroy` réservés à l’auteur. | — |
| [OWASP/AAA] Projets: seul l’auteur peut mettre à jour/supprimer | Oui | `softdesk/permissions.py` → `IsAuthor`; `ProjectViewSet.get_permissions` | `update/partial_update/destroy` réservés à l’auteur (soft-delete). | — |
| [OWASP/AAA] Création restreinte aux contributeurs du projet | Oui | `softdesk/permissions.py` → `IsProjectContributor.has_permission`; `softdesk/mixins.py` → `ParentLookupMixin.perform_create` | Vérifie l’appartenance au projet via `project`/`issue` en query avant `save`. | — |
| [OWASP] Gestion des dépendances via gestionnaire dédié | Oui | `pyproject.toml` (Poetry) | Dépendances et lock gérés par Poetry. | — |
| Authentification par JWT | Oui | `config/settings.py` → REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES, SIMPLE_JWT; `config/urls.py` → `api/token/` | L’API utilise SimpleJWT pour émettre et vérifier des tokens d’accès et de rafraîchissement. | — |
| Accès protégé par défaut | Oui | `config/settings.py` → REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES = IsAuthenticated | Tous les endpoints exigent l’authentification par défaut. | — |
| Durée de vie des tokens raisonnable | Partiel | `config/settings.py` → SIMPLE_JWT.ACCESS_TOKEN_LIFETIME=8h | 8h est relativement long. Bonnes pratiques : 5–15 min, selon le contexte. | Réduire ACCESS_TOKEN_LIFETIME (ex. 15 min) et s’appuyer sur le refresh token. |
| Rotation/blacklist des refresh tokens | Non | — | La rotation/blacklist n’est pas configurée. | Activer ROTATE_REFRESH_TOKENS et BLACKLIST_AFTER_ROTATION et ajouter l’app de blacklist SimpleJWT. |
| Permissions objet : seul l’auteur modifie/supprime | Oui | `softdesk/permissions.py` → IsAuthor; `softdesk/views.py` → get_permissions | Les actions update/partial_update/destroy vérifient l’auteur. | — |
| Cloisonnement par projet (contributeurs uniquement) | Oui | `softdesk/views.py` → get_queryset des ViewSets; `softdesk/permissions.py` → IsProjectContributor; `softdesk/serializers.py` → IssueSerializer (assignee limité) | Les listes filtrent par auteur/contributeurs; l’affectation d’issue ne cible que les contributeurs du projet. | — |
| Soft-delete des projets | Oui | `softdesk/views.py` → ProjectViewSet.perform_destroy; `softdesk/models.py` → Project.is_deleted | La suppression marque is_deleted=True et les requêtes filtrent is_deleted=False. | — |
| Validation âge minimum (RGPD ≥ 15 ans) | Oui | `users/serializers.py` → validate_birth_date | Empêche l’inscription d’un utilisateur de moins de 15 ans. | — |
| [RGPD] Droit d’accès/rectification du profil | Oui | `users/views.py` → `UserViewSet` (IsSelfOrAdmin), `get_queryset` | Chaque utilisateur peut voir/mettre à jour son profil; admin voit tout. | — |
| [RGPD] Droit à l’oubli (suppression complète) | Oui | `users/views.py` → `destroy` via `IsSelfOrAdmin`; `models` → on_delete=CASCADE | L’utilisateur peut supprimer son compte; données liées sont supprimées (CASCADE) ou nettoyées. | Vérifier le périmètre légal selon besoin réel. |
| Consentement (peut être contacté / données partagées) | Oui | `users/models.py` → can_be_contacted, can_data_be_shared (False par défaut) | Champs dédiés avec valeur par défaut à False (privacy by default). | — |
| Hashage des mots de passe | Oui | `users/serializers.py` → create() utilise create_user | Utilise le mécanisme Django pour hasher le mot de passe. | — |
| Complexité mots de passe | Oui | `config/settings.py` → AUTH_PASSWORD_VALIDATORS | Validators standards (longueur, communs, numériques). | — |
| Pagination des listes | Non | — | Aucune pagination DRF définie. | Définir DEFAULT_PAGINATION_CLASS et PAGE_SIZE (ou pagination par vue). |
| Limitation de débit (rate limiting) | Non | — | Pas de throttling sur les endpoints sensibles ni global. | Configurer DEFAULT_THROTTLE_CLASSES et DEFAULT_THROTTLE_RATES; en particulier sur login/JWT. |
| Sécurité production : SECRET_KEY protégé | Non | `config/settings.py` → SECRET_KEY en clair | La clé secrète est hardcodée dans le dépôt. | Charger la clé via variables d’environnement; ne pas la commiter. |
| Sécurité production : DEBUG désactivé | Non | `config/settings.py` → DEBUG=True | DEBUG doit être False en prod. | Piloter DEBUG par env var (False en prod). |
| Sécurité production : ALLOWED_HOSTS définis | Non | `config/settings.py` → ALLOWED_HOSTS=[] | Doit lister les hôtes autorisés. | Renseigner les domaines/IP en prod (env var). |
| Forcer HTTPS, HSTS, cookies sécurisés | Non | — | Pas de SECURE_SSL_REDIRECT, HSTS, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, etc. | Activer ces réglages en prod derrière HTTPS. |
| En-têtes de sécurité (X-Frame-Options, nosniff) | Partiel | `MIDDLEWARE` inclut `SecurityMiddleware`, `XFrameOptionsMiddleware` | X-Frame-Options est actif; nosniff dépend des settings (généralement True). | Vérifier/forcer `SECURE_CONTENT_TYPE_NOSNIFF=True` et autres paramètres associés. |
| CSRF (selon mécanisme d’auth) | Partiel | `MIDDLEWARE` inclut `CsrfViewMiddleware`; Auth inclut `SessionAuthentication` | Avec JWT stateless, CSRF ne s’applique pas. SessionAuthentication active CSRF pour le navigateur. | En prod API pure, envisager de retirer SessionAuthentication. |
| CORS (si front sur autre domaine) | À vérifier | — | Non configuré dans le code. | Ajouter `django-cors-headers` si des frontends cross-domain existent. |
| Journalisation sécurité / audit | Non | — | Pas de configuration de logging de sécurité détectée. | Configurer LOGGING (accès, erreurs, sécurité), corréler avec reverse proxy. |
| Gestion des erreurs (pas d’info sensible) | Partiel | — | Dépend de DEBUG. | Mettre DEBUG=False, pages d’erreurs neutres, logs privés. |
| Minimisation/exposition de données | Partiel | `users/serializers.py`, `softdesk/serializers.py` | Champs exposés OK globalement. `IssueSerializer` utilise `fields='__all__'`. | Restreindre aux champs nécessaires; éviter `__all__` côté API publique. |
| Intégrité des serializers (Comment) | Non | `softdesk/serializers.py` → `CommentSerializer.read_only_fields` contient `project` inexistant | Incohérence susceptible de provoquer une erreur DRF (champ non défini). | Retirer `project` de `read_only_fields`. |
| Intégrité des serializers (Project) | Non | `softdesk/serializers.py` → `ProjectSerializer.read_only_fields` inclut `updated_time` inexistant | Champ non présent sur le modèle ni dans `fields`. | Retirer `updated_time` ou ajouter le champ sur le modèle/le serializer. |
| Import du modèle User correct | Non | `softdesk/serializers.py` → `from .models import ..., User` | `User` n’est pas défini dans `softdesk.models`. | Remplacer par `from users.models import User`. |
| Optimisation requêtes (green code) | Partiel | `softdesk/views.py` | Pas de `select_related/prefetch_related`; filtres corrects. | Ajouter `select_related` (ex. issue→project, comment→issue,author) et `prefetch_related` sur M2M. |
| Dépendances gérées/pinnées | Oui | `pyproject.toml` (Poetry) | Dépendances déclarées et lockées. | — |
| Surveillance dépendances (Dependabot) | Non | — | Non présent dans le repo. | Ajouter `.github/dependabot.yml` pour pip/poetry et GitHub Actions. |

---

## Détails et extraits par thème

### 1) Authentification & permissions
- JWT activé
  - `config/settings.py` → REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES inclut `rest_framework_simplejwt.authentication.JWTAuthentication`.
  - `config/urls.py` expose `api/token/` et `api/token/refresh/`.
- Accès par défaut authentifié
  - `config/settings.py` → DEFAULT_PERMISSION_CLASSES = `IsAuthenticated`.
- Contrôles d’accès fins
  - `softdesk/permissions.py` → `IsAuthor`, `IsProjectContributor`.
  - `softdesk/views.py` filtre les queryset pour ne renvoyer que les objets de l’auteur/contributeurs.
  - `softdesk/serializers.py` → `IssueSerializer` restreint `assignee` aux contributeurs du projet (incluant l’auteur).

### 2) RGPD (âge, consentement, minimisation)
- Âge ≥ 15 ans
  - `users/serializers.py` → `validate_birth_date` calcule l’âge et lève une erreur si <15.
- Consentements explicites par défaut « non »
  - `users/models.py` → `can_be_contacted=False`, `can_data_be_shared=False`.
- Accès aux seules données propres (hors admin)
  - `users/views.py` → `get_queryset` restreint aux données de l’utilisateur courant sauf `is_staff`.

### 3) Sécurité opérationnelle (prod)
- Clé secrète, DEBUG, ALLOWED_HOSTS
  - `config/settings.py` → SECRET_KEY en clair, DEBUG=True, ALLOWED_HOSTS=[]. À externaliser et durcir en prod.
- En-têtes & HTTPS
  - `SecurityMiddleware` et `XFrameOptionsMiddleware` présents. Manquent HSTS/redirect/cookies sécurisés explicites.

### 4) Robustesse API
- Pagination et throtlling
  - Non configurés. À ajouter pour UX et sécurité (anti-brute-force, DoS applicatif).
- Validation
  - Choix/contraintes dans `softdesk/models.py` (choices pour status, priority, tag). Bug à corriger dans `CommentSerializer.read_only_fields`.
- Logs
  - Aucun LOGGING spécifique. À configurer.

### 5) Optimisation (green code)
- Requêtes
  - Ajouter `select_related('project','author')` sur Issue; `select_related('issue','author','issue__project')` sur Comment; `prefetch_related('contributors')` sur Project.
- Pagination
  - Indispensable pour limiter charge et latence côté client.

---

## Corrections proposées (sans modifier le code ici)

1) Sécuriser les settings de production
- Charger `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` via variables d’environnement.
- Activer `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS` (ex. 31536000), `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`, `SECURE_HSTS_PRELOAD=True` (si éligible).

2) JWT
- Réduire `ACCESS_TOKEN_LIFETIME` (ex. 15 min), garder `REFRESH_TOKEN_LIFETIME` (ex. 7 jours).
- Activer la rotation et le blacklist (SimpleJWT blacklist app) si requis par le PDF.

3) DRF
- Pagination globale : `DEFAULT_PAGINATION_CLASS` (LimitOffset ou PageNumber) + `PAGE_SIZE`.
- Throttling : `DEFAULT_THROTTLE_CLASSES` (UserRateThrottle, AnonRateThrottle) + `DEFAULT_THROTTLE_RATES` (ex. user:1000/jour, anon:100/jour) et règles spécifiques sur l’auth.

4) Serializers
- Remplacer `fields='__all__'` par une liste explicite dans `IssueSerializer`.
- Retirer le champ inexistant `project` de `CommentSerializer.read_only_fields`.

5) Optimisation requêtes
- Ajouter `select_related`/`prefetch_related` dans les `get_queryset` appropriés.

6) Dépendances
- Ajouter `.github/dependabot.yml` pour Poetry/pip.

7) CORS (si besoin)
- Installer/configurer `django-cors-headers` pour autoriser explicitement les origines nécessaires.

---

## Couverture des exigences du PDF (détail)

1) OWASP / AAA
- Authentification (JWT): Oui – Voir « Authentification par JWT » et réglages SimpleJWT.
- Autorisation (accès aux projets/ressources): Oui – Filtrage par contribution + permissions objet.
- Accès (update/delete par l’auteur uniquement): Oui – `IsAuthor` appliqué sur update/destroy.
- Gestion des dépendances: Oui – Poetry en place.

2) RGPD
- Droit d’accès et rectification: Oui – Accès restreint au profil propre, admin global.
- Droit à l’oubli: Oui – Suppression de compte possible; FKs en CASCADE assurent le nettoyage.
- Collecte du consentement: Oui – Champs booléens explicites avec défaut à False.
- Vérification de l’âge ≥ 15 ans: Oui – Validation à la création.

3) Green code
- Pagination: Non – À ajouter (obligatoire selon le PDF pour sobriété côté serveur/clients).
- Optimisation ORM: Partiel – Sélection/Préchargement manquants; recommandations listées.

Remarque: Des durcissements de sécurité opérationnelle (DEBUG/SECRET_KEY/ALLOWED_HOSTS, HTTPS/HSTS, throttling, CORS, logging) sont recommandés bien qu’ils ne soient pas explicitement listés dans le PDF, et sont standard en prod.

