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
```bash
# cloner
git clone <https://github.com/MaximeJB/softdesk/>
cd SoftDesk

# installer dépendances
poetry install
