Mission
SoftDesk, une société d'édition de logiciels de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques. Cette solution, SoftDesk Support, s’adresse à des entreprises en B2B (Business to Business). 
 
 
 
SoftDesk a mis en place une nouvelle équipe chargée de ce projet et vous avez été embauché comme ingénieur logiciel pour créer un back-end performant et sécurisé, devant servir des applications front-end sur différentes plateformes. Il faut alors trouver un moyen standard de traiter les données, ce qui peut se faire en développant une API RESTful. 


Une fois installé au bureau, vous décidez de contacter Alex, le responsable technique avec qui vous avez eu votre dernier entretien, pour vous aider sur la première phase du projet. Il vous répond avec plus de détails sur la mise en œuvre de l'API :
 
De : Alex
À : Vous
Objet : Mise en œuvre de l'API 
Bonjour,
J'espère que tout se passe bien au cours de ces premiers jours chez SoftDesk. Comme convenu, je te transmets les documents nécessaires pour t’aider à commencer le développement de notre API : un document de la conception de la mise en œuvre et un document liste des vérifications.


Le fichier conception de la mise en œuvre contient le diagramme qui t’aidera à identifier :
•	les modèles d'objets ; 
•	les principales fonctionnalités de l’application ; 
•	ainsi qu'une liste des points de terminaison d'API requis et un exemple de réponse.
Le fichier exigences de sécurité et d’optimisation contient les besoins liés à la sécurité et à notre engagement dans le green code : 
•	Les spécifications OWASP répertorient les mesures de sécurité OWASP que le back-end doit respecter. L’API devra authentifier les utilisateurs à l’aide de Json Web Token (JWT) et définir des permissions d’accès aux ressources par groupe d’utilisateurs ;
•	Les spécifications RGPD appliquent les règles de protection de la donnée et la confidentialité de chaque utilisateur. L’API devra s’assurer que les utilisateurs puissent protéger leurs données et spécifier s’ils souhaitent ou non être contactés via un champ de formulaire spécifique ;
•	Les spécifications green code répertorient les mesures de conceptions « green », qui permettent d’optimiser et de simplifier le code, dans un but de sobriété énergétique. L’API devra tendre vers une utilisation optimisée des requêtes pour éviter la surconsommation des serveurs. 

Je te suggère d'étudier soigneusement la conception et d'identifier les modèles d'objets pour, enfin, commencer à coder. 

N'hésite pas à me contacter si tu as besoin de clarifications. 


Cordialement,
Alex
Pièces jointes :
•	Conception de la mise en œuvre
•	Exigences de sécurité et d'optimisation

 
Maintenant que vous êtes en possession des détails du produit et des spécifications requises pour l'application, vous voilà prêt à démarrer le projet ! 
Étapes
Prenez le temps de bien cadrer le projet avant de le démarrer. Ne le commencez pas s’il comporte encore trop de zones d’ombres. Bien entendu, vous pourrez en éclaircir certaines lors de l’implémentation, mais une bonne préparation vous permettra d’avancer dans de meilleures conditions.

Django Rest Framework est une surcouche à Django et permet entre autres d’automatiser la gestion CRUD (Create, Read, Update, Delete) de vos modèles sous forme d’API. Prenez le temps d’assimiler ses mécanismes et utilisez toute sa puissance en implémentant les ModelViewsets.

Déterminez une stratégie de tests en définissant des chemins utilisateurs. Une API REST ne retourne que de la donnée brute, mais vous pouvez tout de même savoir quelle requête sera utile par quel utilisateur. Par exemple, la création de l’utilisateur est propre à la phase d’inscription. La création d’un contributeur est propre à la souscription d’un utilisateur vers un projet. La création d’un commentaire se fait lorsqu’un contributeur souhaite réagir à un problème particulier… Réfléchir de cette manière permettra de donner du sens à votre implémentation et à vos tests.
Etape 1 : Démarrez le projet et identifier le besoin
Prérequis
•	avoir étudié les notes ainsi que les documents Conception de la mise en œuvre et Exigences de sécurité et d'optimisation ;
•	avoir identifié les modèles d’objets dans le diagramme des relations du système de suivi des problèmes du document Conception de la mise en œuvre.
Résultat attendu
•	avoir configuré le projet ;
•	avoir versionné le projet sur Github, avec un fichier README expliquant l’installation et le lancement du projet en local.
Recommandations  
•	Prenez le temps de bien comprendre le besoin ;
•	Le diagramme libre dans le document Conception de la mise en œuvre, sans formalisme particulier, permet d’identifier les différents modèles de données présents dans l’application. C’est sur cette base que vous pourrez, si vous le souhaitez, élaborer des diagrammes plus précis, de classe ou d’entité/relation, par exemple. Dans tous les cas, il peut être intéressant de se renseigner sur les différents types de diagrammes qui peuvent aider à la conception d’une application ;
•	Ces différentes ressources se caractérisent par des modèles dans l’ORM de Django, et définissent à la fois la table SQL et la classe Python. Il sera nécessaire de penser les différents attributs pour chaque modèle ;
•	Le diagramme propose aussi des liens entre chaque ressource, qui caractérisent les différentes relations qu’elles peuvent avoir entre elles. Encore une fois, ce sera à vous de définir la nature de ces relations (One To One, One To Many ou Many To Many…) ;
•	Créez les attributs nécessaires à chacun de vos modèles ;
•	Remplacez votre utilisation de pip par Pipenv ou Poetry afin de sécuriser la gestion des dépendances entre elles.
 
Point de vigilance
•	Attention : une erreur serait de se plonger directement dans le code alors que le projet n’a pas été assez cadré.
 Etape 2 : Définissez les utilisateurs
Prérequis
•	avoir défini les attributs des modèles de données ;
•	avoir pensé et spécifié les différentes routes que les utilisateurs pourront prendre.
Résultat attendu
•	avoir mis en place le modèle User.
Recommandations
•	Pensez à créer une app Django spécifique pour le modèle User ;
•	Redéfinissez le modèle User de base de Django. C’est une bonne pratique encouragée par l’équipe de Django ;
•	Créez le modèle, puis serialisez-le. Passez enfin à la vue (renseignez-vous le système de ModelViewset de Django Rest Framework) ;
•	Finalisez l’implémentation avec la mise en place du router ;
•	Vérifiez l’implémentation par le biais de l’application Postman, et assurez-vous de pouvoir créer, lire, modifier et supprimer un utilisateur.
Points de vigilance
•	Attention à bien réfléchir aux relations entre les modèles (OneToMany, ManyToMany, OneToOne…). Ici, nous n’implémentons que le modèle User, mais lorsque vous implémenterez les autres modèles, il sera nécessaire de repenser les relations avec les modèles existants ;
•	Il est important de vérifier le bon fonctionnement de chaque partie de son code. N’hésitez pas à utiliser la commande “python manage.py shell” pour entrer dans l’application Django et manipuler les objets, comprendre leurs intéractions ; 
•	Enfin, Postman est l’étape décisive pour vérifier que le serveur répond aux requêtes utilisateurs ;
•	Attention, dans le respect des normes RGPD, un utilisateur de moins de 15 ans ne devrait pas pouvoir finaliser son inscription.
Etape 3 : définissez les projets et les contributeurs
Prérequis
•	avoir implémenté et testé le modèle User.
Résultat attendu
•	avoir implémenté et testé les modèles Application et Contributor.
Recommandations 
•	Réfléchissez au découpage de votre projet. Devez-vous créer une ou plusieurs app Django ? Le contributeur est-il plus proche du modèle utilisateur ou du modèle projet ? Un bon découpage du code permet de mieux le comprendre et ainsi, de faciliter sa mise en place ;
•	Implémentez le modèle Project avant le modèle Contributor. En effet, le Contributor ne peut fonctionner sans Project ; 
•	Pensez au cas où le Contributor serait aussi l’auteur du projet (son créateur).
Point de vigilance
•	Encore une fois, prenez le temps de bien tester les différentes URL de votre application pour vous assurer de son bon fonctionnement.

Etape 4 : définissez les problèmes et les commentaires
Prérequis
•	avoir implémenté et testé les modèles Project et Contributor.
Résultat attendu
•	avoir implémenté et testé les modèles Issue et Comment.
Recommandation 
•	L’implémentation de ces deux modèles de données est relativement similaire. La mise en place de l’un facilite donc celle de l’autre.
Points de vigilance
•	Pensez à l’architecture de votre code ;
•	Testez chaque point de terminaison (URL de l’application).

Etape 5 : mettez en place le système de permissions
Prérequis
•	avoir implémenté et testé les différents modèles de données de l’application.
Résultat attendu
•	avoir implémenté et testé le système de permissions ;
•	avoir ajouté le dependabot au repository Github.
Recommandations
•	Il est maintenant temps d’ajouter des permissions à l’application ! Commencez par ajouter la permission d’authentification à l’aide d’un Json Web Token ;
•	Implémentez ensuite les permissions de lecture et d’écriture sur chaque ressource. L’auteur d’une ressource a tous les droits dessus, mais les autres utilisateurs ne peuvent que lire la ressource ou la référencer dans une autre ressource ;
•	Utilisez le système de classes de permissions fourni dans Django Rest Framework pour créer des permissions sur les vues ;
•	Pensez aussi à la confidentialité des données : vérifiez bien que l’utilisateur possède les champs définis dans notre application des normes RGPD.
Points de vigilance
•	Il ne s’agira plus de tester simplement les opérations Create, Read, Update, Delete sur chaque ressource, mais de vérifier ces différentes opérations selon le type d’utilisateur (non authentifié, authentifié, contributeur, auteur…) ;
•	Le « droit à l’oubli » est une règle qui dit qu’un utilisateur doit pouvoir supprimer ses données personnelles sans subsistance dans la base de données de l’application cible. Dans le cadre de cette application, ce droit à l’oubli se résout automatiquement lors de la suppression, mais certaines applications remplacent la suppression réelle par une « fausse suppression », appelée « soft delete ».
Pensez green code et optimisez l’application
Prérequis
•	avoir implémenté et testé les différents modèles de données de l’application ;
•	avoir sécurisé l’application.
Résultat attendu 
•	avoir optimisé l’application pour la rendre moins gourmande en ressources ;
•	avoir implémenté la pagination.
Recommandations 
•	Vérifiez que votre application ne possède pas de trop grandes imbrications des ressources. Ce projet ne demande pas d’imbriquer les ressources entre elles, c’est donc à vous de décider si vous souhaitez ou non imbriquer les ressources dans le corps de réponse de la requête. Cependant, contentez-vous d’un seul niveau d’imbrication pour éviter de retourner des requêtes trop volumineuses ;
•	Django Rest Framework possède un système de pagination puissant et simple à mettre en place. N’hésitez pas à parcourir la documentation associée.
Point de vigilance
•	Réfléchissez bien lors de l’implémentation de la pagination. Combien de ressources souhaitez-vous fournir par page ? Des pages trop petites demanderont de créer plus de requêtes pour accéder aux différentes ressources. Mais des pages trop grandes augmentent drastiquement le poids de chaque requête.
