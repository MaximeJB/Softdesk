# SoftDesk

API REST minimaliste pour gérer des projets collaboratifs (projets, contributeurs, issues, commentaires) — prototype Django + DRF.

---

## Présentation rapide
SoftDesk permet à des utilisateurs de créer des projets, d’ajouter des contributeurs, de créer/assigner des issues (bugs, features, tasks) et d’échanger via des commentaires.  
Authentification par JWT (djangorestframework-simplejwt). 
Permissions fines (auteur vs contributeur). 
Optimisations ORM (`select_related` / `prefetch_related`) pour limiter les requêtes.

---

## Fonctions principales
- Gestion utilisateurs (inscription, login JWT)
- Projets : création, type (backend/frontend/ios/android), auteur, contributeurs
- Issues : statut, priorité, tag, attribution à un contributeur
- Commentaires rattachés aux issues
- Permissions : contributeurs accèdent aux ressources du projet ; seul l’auteur peut modifier/supprimer sa ressource
- Validation RGPD de base (consentements, âge minimum)

---

## RGPD & OWASP (chapitre dédié)

- Consentements : champs (`can_be_contacted`) et (`can_data_be_shared`) collectés à l'inscription.
- Âge minimum : validation (≥ 15 ans) dans le serializer d'inscription.
- Minimisation des données exposées : les réponses exposent l’author par username 
- Droit à l’oubli / anonymisation : modèles configurables pour on_delete=SET_NULLafin de permettre anonymisation plutôt que perte de données collectives.
- Authentification : JWT (djangorestframework-simplejwt) pour sécuriser l’accès API.
- Permissions fines : IsAuthor, IsCollab, IsAuthorOfProject pour contrôler lecture/écriture au niveau objet.
- Protection contre N+1 : utilisation de select_related / prefetch_related pour limiter les requêtes inutiles.
- Pas d’exposition de passwords : champs password en (`write_only`) dans les serializers.

## Installation (complète)

### Prérequis
- Python 3.10+ (compatible 3.12)
- Poetry
- Git
- (optionnel) PostgreSQL / autre base si voulu (par défaut SQLite)

### Installation locale (avec Poetry)

**Étape 1 : Cloner le repository**
```bash
git clone https://github.com/MaximeJB/softdesk/
cd SoftDesk
```

**Étape 2 : Installer les dépendances**
```bash
poetry install
```

**Étape 3 : Activer l'environnement virtuel**
```bash
poetry shell
```

**Étape 4 : Appliquer les migrations de base de données**
```bash
python manage.py migrate
```

**Étape 5 (optionnel) : Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

**Étape 6 : Démarrer le serveur**
```bash
python manage.py runserver
```

Le projet est maintenant accessible sur `http://127.0.0.1:8000/`

---

## Utilisation de l'API

### Authentification

**1. Créer un compte utilisateur**
```bash
POST http://127.0.0.1:8000/users/
Content-Type: application/json

{
  "username": "john",
  "password": "Pass123!",
  "email": "john@example.com",
  "age": 25,
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

**2. Obtenir un token JWT**
```bash
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
  "username": "john",
  "password": "Pass123!"
}
```

Réponse : `{"access": "...", "refresh": "..."}`

**3. Utiliser le token dans les requêtes**
```bash
Authorization: Bearer <access_token>
```

### Endpoints disponibles

**Projets**
```bash
GET    /projects/              # Liste des projets
POST   /projects/              # Créer un projet (type: backend/frontend/ios/android)
GET    /projects/{id}/         # Détails d'un projet
PUT    /projects/{id}/         # Modifier (auteur uniquement)
DELETE /projects/{id}/         # Supprimer (auteur uniquement)
```

**Contributeurs**
```bash
GET    /projects/{id}/contributors/       # Liste des contributeurs
POST   /projects/{id}/contributors/       # Ajouter un contributeur (auteur uniquement)
DELETE /projects/{id}/contributors/{id}/  # Retirer un contributeur (auteur uniquement)
```

**Issues**
```bash
GET    /projects/{id}/issues/           # Liste des issues
POST   /projects/{id}/issues/           # Créer (priority: low/medium/high, tag: bug/feature/task)
GET    /projects/{id}/issues/{id}/      # Détails
PUT    /projects/{id}/issues/{id}/      # Modifier (auteur de l'issue uniquement)
DELETE /projects/{id}/issues/{id}/      # Supprimer (auteur de l'issue uniquement)
```

**Commentaires**
```bash
GET    /projects/{id}/issues/{id}/comments/       # Liste des commentaires
POST   /projects/{id}/issues/{id}/comments/       # Créer un commentaire
GET    /projects/{id}/issues/{id}/comments/{id}/  # Détails
PUT    /projects/{id}/issues/{id}/comments/{id}/  # Modifier (auteur uniquement)
DELETE /projects/{id}/issues/{id}/comments/{id}/  # Supprimer (auteur uniquement)
