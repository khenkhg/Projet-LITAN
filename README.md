# LITAN – Site Officiel du Laboratoire de Recherche (ESTIN)

Site web officiel et espace de travail du laboratoire de recherche **LITAN** (*Laboratoire d'Informatique Théorique et Appliquée de Nâama / ESTIN*), Béjaïa, Algérie.

## 🚀 Stack Technique

* **Frontend** : React 18, Vite, TypeScript, React Router 6, TanStack Query 5, Tailwind CSS, react-i18next.
* **Backend** : Python 3.12, Django 5, Django REST Framework, django-allauth (Google Workspace `@estin.dz`).
* **Base de données** : PostgreSQL 16.
* **Génération PDF** : WeasyPrint.
* **Infrastructure** : Docker Compose (PostgreSQL, Django, Frontend servi par Nginx en reverse-proxy).

---

## 🛠️ Démarrage Rapide avec Docker Compose

### 1. Prérequis
* Docker Desktop installé et démarré (avec support `docker-compose`).

### 2. Configuration de l'environnement
Copiez le fichier d'exemple si `.env` n'existe pas encore :
```bash
cp .env.example .env
```
*(Les valeurs par défaut conviennent pour le développement local).*

### 3. Lancer les conteneurs
```bash
docker-compose up --build
```
Les services démarrent :
* `litan_db` (PostgreSQL 16) sur le port 5432
* `litan_backend` (Django 5) sur le port 8000
* `litan_frontend` (Nginx + React) sur le port 80

### 4. Initialiser la base de données et créer un super-administrateur
Dans un autre terminal :
```bash
# Appliquer les migrations
docker-compose exec backend python manage.py migrate

# Créer un compte administrateur
docker-compose exec backend python manage.py createsuperuser
```

---

## 🌐 Accès aux Services

* **Site web principal (Vitrine + Espace Membres)** : [http://localhost](http://localhost)
* **Interface d'administration Django** : [http://localhost/admin/](http://localhost/admin/) (ou direct [http://localhost:8000/admin/](http://localhost:8000/admin/))
* **API REST** : [http://localhost/api/](http://localhost/api/)

---

## 📁 Structure du Projet

```
.
├── backend/
│   ├── apps/
│   │   ├── accounts/       # Utilisateurs (@estin.dz), profils, conformité Loi 18-07
│   │   ├── teams/          # Équipes de recherche et redirections d'URL
│   │   ├── publications/   # Publications, auteurs, BibTeX, import DOI
│   │   ├── works/          # Travaux des membres (projets, stages, encadrements)
│   │   ├── news/           # Actualités du laboratoire et des équipes
│   │   ├── equipment/      # Équipements et plateformes scientifiques
│   │   ├── offers/         # Offres de stages, PFE, thèses et post-docs
│   │   ├── useful_links/   # Liens utiles (publics ou réservés membres)
│   │   └── lab_settings/   # Paramètres globaux et présentation du labo
│   ├── config/             # Configuration Django (settings, urls, wsgi)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # AppShell, Header réactif, Footer
│   │   ├── locales/        # Traductions (fr/translation.json, prêt pour en)
│   │   ├── pages/          # Pages de l'application
│   │   └── services/       # Client API Axios avec CSRF et credentials
│   ├── Dockerfile
│   └── nginx.conf          # Reverse proxy Nginx
├── docs/
│   ├── PROJECT_BRIEF.md    # Règles de développement et périmètre
│   └── cahier_des_charges.pdf # Source de vérité officielle
└── docker-compose.yml
```
