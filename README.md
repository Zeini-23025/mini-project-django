
# 📚 Gestion de Bibliothèque - Application Web Django

Une application web de gestion de bibliothèque permettant à un administrateur de gérer les livres, catégories, emprunts, utilisateurs et historique. Les utilisateurs peuvent consulter les livres, emprunter et retourner des ouvrages.

## 🌐 Technologies utilisées

- Python 3.x
- Django 4.x
- SQLite (par défaut, peut être remplacé par MySQL ou PostgreSQL)
- HTML/CSS (Bootstrap)

---

## 📁 Structure du projet

```
getionbibliotheque/
├── getionbibliotheque/         # Répertoire principal Django
│   ├── settings.py       # Configuration globale
│   ├── urls.py           # Routes globales
│   └── wsgi.py
├── bibliotheque/              # Application principale
│   ├── models.py         # Modèles: Livre, Emprunt, Categorie, Historique
│   ├── views.py          # Vues utilisateur/admin
│   ├── urls.py           # Routes de l'app
│   ├── templates/
│   │   ├── admin/        # Pages HTML pour l'admin
│   │   └── user/         # Pages HTML pour les utilisateurs
│   └── forms.py          # Formulaires personnalisés
├── db.sqlite3            # Base de données par défaut
├── manage.py             # Commande pour gérer le projet
└── static/               # Fichiers CSS/JS (si configurés)
```

---

## ✅ Fonctionnalités principales

### 👨‍💼 Administrateur :
- Connexion sécurisée
- Tableau de bord avec statistiques
- Gestion des livres (CRUD)
- Gestion des catégories (CRUD)
- Gestion des emprunts et retours
- Suivi de l’historique

### 👤 Utilisateur :
- Inscription / Connexion
- Consultation des livres et catégories
- Emprunter et retourner un livre
- Voir ses emprunts en cours
- Consulter son historique

---

## 🚀 Comment exécuter le projet localement

### 1. Cloner le projet
```bash
git clone https://github.com/Zeini-23025/mini-project-django.git
cd mini-project-django
```

### 2. Créer un environnement virtuel
```bash
python -m venv env
source env/bin/activate  # sous Windows : env\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

> Si `requirements.txt` n'existe pas, installe manuellement :
```bash
pip install django django-widget-tweaks
```

### 4. Appliquer les migrations
```bash
python manage.py migrate 
```

### 5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

Ensuite, ouvre ton navigateur à l’adresse :  
👉 `http://127.0.0.1:8000/`

---

---

### avec docker

```
docker build -t monapp-django .
```

```
docker run -p 8000:8000 monapp-django
```


---

## ✍️ Auteur

Projet développé par Zeini.

---

