from django.urls import path
from . import views

urlpatterns = [
    # Routes pour les administrateurs
    path('admin/livres/', views.liste_livres, name='liste_livres'),
    path('admin/livres/ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('admin/livres/modifier/<int:pk>/', views.modifier_livre, name='modifier_livre'),
    path('admin/livres/supprimer/<int:pk>/', views.supprimer_livre, name='supprimer_livre'),

    path('admin/categories/', views.liste_categories, name='liste_categories'),
    path('admin/categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('admin/categories/modifier/<int:pk>/', views.modifier_categorie, name='modifier_categorie'),
    path('admin/categories/supprimer/<int:pk>/', views.supprimer_categorie, name='supprimer_categorie'),

    path('admin/emprunts/', views.liste_emprunts, name='liste_emprunts'),
        path('bibliotheque/admin/emprunts/retourner/<int:pk>/', views.retourner_emprunt_admin, name='retourner_emprunt_admin'),
    path('admin/emprunts/ajouter/', views.ajouter_emprunt, name='ajouter_emprunt'),

    path('admin/historique/', views.liste_historique, name='liste_historique'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/home/', views.admin_home, name='admin_home'),

    # Routes pour les utilisateurs
    path('user/home/', views.user_home, name='user_home'),  # Page d'accueil utilisateur

    path('user/livres/', views.liste_livres_user, name='liste_livres_user'),  # Liste des livres pour l'utilisateur
    path('user/categories/', views.liste_categories_user, name='liste_categories_user'),  # Liste des catégories pour l'utilisateur

    path('user/mes_livres_empruntes/', views.mes_livres_empruntes, name='mes_livres_empruntes'),  # Mes livres empruntés
    path('user/mon_historique/', views.mon_historique, name='mon_historique'),  # Mon historique d'emprunt
    path('signup/', views.signup_view, name='signup'),
        path('user/livres/emprunter/<int:livre_id>/', views.emprunter_livre, name='emprunter_livre'),
       path('bibliotheque/user/emprunts/retourner/<int:pk>/', views.retourner_emprunt_user, name='retourner_emprunt_user'),
    ]
