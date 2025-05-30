from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Livre, Categorie, Emprunt, Historique
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

# Décorateur personnalisé pour vérifier que l'utilisateur est un administrateur

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Rediriger vers la page de login si l'utilisateur n'est pas connecté
        if not request.user.is_superuser:
            return redirect('user_home')  # Rediriger vers la page utilisateur si ce n'est pas un administrateur
        return view_func(request, *args, **kwargs)  # Appeler la vue si l'utilisateur est un admin
    return _wrapped_view

# Vue pour afficher la liste des livres (admin)
@admin_required
def liste_livres(request):
    livres = Livre.objects.all()
    return render(request, 'admin/livres.html', {'livres': livres})

# Vue pour ajouter un livre (admin)
@admin_required
def ajouter_livre(request):
    if request.method == 'POST':
        titre = request.POST['titre']
        auteur = request.POST['auteur']
        genre_id = request.POST['genre']
        annee_publication = request.POST['annee_publication']
        exemplaires = request.POST['exemplaires_disponibles']
        genre = get_object_or_404(Categorie, id=genre_id)
        Livre.objects.create(
            titre=titre,
            auteur=auteur,
            genre=genre,
            annee_publication=annee_publication,
            exemplaires_disponibles=exemplaires
        )
        return redirect('liste_livres')

    categories = Categorie.objects.all()
    return render(request, 'admin/ajouter_livre.html', {'categories': categories})

# Vue pour modifier un livre (admin)
@admin_required
def modifier_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    if request.method == 'POST':
        livre.titre = request.POST['titre']
        livre.auteur = request.POST['auteur']
        genre_id = request.POST['genre']
        livre.genre = get_object_or_404(Categorie, id=genre_id)
        livre.annee_publication = request.POST['annee_publication']
        livre.exemplaires_disponibles = request.POST['exemplaires_disponibles']
        livre.save()
        return redirect('liste_livres')

    categories = Categorie.objects.all()
    return render(request, 'admin/modifier_livre.html', {'livre': livre, 'categories': categories})

# Vue pour supprimer un livre (admin)
@admin_required
def supprimer_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    livre.delete()
    return redirect('liste_livres')

# Vue pour afficher la liste des catégories (admin)
@admin_required
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'admin/categories.html', {'categories': categories})

# Vue pour ajouter une catégorie (admin)
@admin_required
def ajouter_categorie(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        Categorie.objects.create(nom=nom)
        return redirect('liste_categories')
    return render(request, 'admin/ajouter_categorie.html')

# Vue pour modifier une catégorie (admin)
@admin_required
def modifier_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        categorie.nom = request.POST['nom']
        categorie.save()
        return redirect('liste_categories')
    return render(request, 'admin/modifier_categorie.html', {'categorie': categorie})

# Vue pour supprimer une catégorie (admin)
@admin_required
def supprimer_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    categorie.delete()
    return redirect('liste_categories')

# Vue pour afficher la liste des emprunts (admin)
@admin_required
def liste_emprunts(request):
    emprunts = Emprunt.objects.filter(retourne=False)
    return render(request, 'admin/emprunts.html', {'emprunts': emprunts})

# Vue pour retourner un emprunt (admin)
@admin_required
def retourner_emprunt_admin(request, pk):
    emprunt = get_object_or_404(Emprunt, id=pk)
    emprunt.retourne = True
    emprunt.date_retour = timezone.now()
    emprunt.save()

    # Ajouter à l'historique
    Historique.objects.create(
        utilisateur=emprunt.utilisateur,
        livre=emprunt.livre,
        date_emprunt=emprunt.date_emprunt,
        date_retour=emprunt.date_retour
    )

    emprunt.delete()  # Supprimer l'emprunt
    emprunt.livre.exemplaires_disponibles += 1
    emprunt.livre.save()

    return redirect('liste_emprunts')

# Vue pour afficher l'historique des emprunts (admin)
@admin_required
def liste_historique(request):
    historique = Historique.objects.all()
    return render(request, 'admin/historique.html', {'historique': historique})

# Vue pour ajouter un emprunt (admin)
@admin_required
def ajouter_emprunt(request):
    if request.method == 'POST':
        utilisateur_id = request.POST['utilisateur']
        livre_id = request.POST['livre']

        utilisateur = get_object_or_404(User, id=utilisateur_id)
        livre = get_object_or_404(Livre, id=livre_id)

        if livre.exemplaires_disponibles > 0:
            Emprunt.objects.create(utilisateur=utilisateur, livre=livre)
            livre.exemplaires_disponibles -= 1
            livre.save()
            return redirect('liste_emprunts')
        else:
            return render(request, 'admin/ajouter_emprunt.html', {'error': "Pas d'exemplaires disponibles"})

    livres = Livre.objects.all()
    users = User.objects.all()
    return render(request, 'admin/ajouter_emprunt.html', {'livres': livres, 'users': users})

# Vue de la page de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('user_home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# Vue de la page de logout
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de login après la déconnexion

# Vue pour la page d'accueil de l'admin (statistiques)
@admin_required
def admin_home(request):
    # Récupérer les statistiques nécessaires
    nombre_livres = Livre.objects.count()
    livres_empruntes = Emprunt.objects.filter(retourne=False).count()  # Nombre de livres non retournés
    nombre_categories = Categorie.objects.count()
    nombre_utilisateurs = User.objects.count()

    # Passer les données à la template
    return render(request, 'admin/admin_home.html', {
        'nombre_livres': nombre_livres,
        'livres_empruntes': livres_empruntes,
        'nombre_categories': nombre_categories,
        'nombre_utilisateurs': nombre_utilisateurs
    })

# Vue pour la page d'accueil de l'utilisateur
from .models import Categorie

@login_required
def user_home(request):
    categories = Categorie.objects.all()  # Récupérer toutes les catégories
    return render(request, 'user/index.html', {'categories': categories})


# Vue pour afficher la liste des livres pour un utilisateur
@login_required
def liste_livres_user(request):
    livres = Livre.objects.all()  # Tous les livres disponibles
    return render(request, 'user/livres.html', {'livres': livres})

# Vue pour afficher la liste des catégories pour un utilisateur
@login_required
def liste_categories_user(request):
    categories = Categorie.objects.all()  # Toutes les catégories
    return render(request, 'user/categories.html', {'categories': categories})

# Vue pour afficher les livres empruntés par l'utilisateur
@login_required
def mes_livres_empruntes(request):
    emprunts = Emprunt.objects.filter(utilisateur=request.user, retourne=False)  # Emprunts non retournés par l'utilisateur
    return render(request, 'user/mes_livres_empruntes.html', {'emprunts': emprunts})

# Vue pour afficher l'historique des emprunts de l'utilisateur
@login_required
def mon_historique(request):
    historique = Emprunt.objects.filter(utilisateur=request.user)  # Historique des emprunts de l'utilisateur
    return render(request, 'user/mon_historique.html', {'historique': historique})


# views.py
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Assure-toi que tu as bien une URL nommée 'login'
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



@login_required
def emprunter_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if livre.exemplaires_disponibles > 0:
        Emprunt.objects.create(utilisateur=request.user, livre=livre)
        livre.exemplaires_disponibles -= 1
        livre.save()
    return redirect('liste_livres_user')
@login_required
def retourner_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id, utilisateur=request.user)
    emprunt.retourne = True
    emprunt.date_retour = timezone.now()
    emprunt.save()

    # Mettre à jour le nombre d'exemplaires disponibles
    emprunt.livre.exemplaires_disponibles += 1
    emprunt.livre.save()

    return redirect('mes_livres_empruntes')
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Livre, Emprunt

@login_required
def retourner_emprunt_user(request, pk):
    emprunt = get_object_or_404(Emprunt, id=pk, utilisateur=request.user)
    emprunt.retourne = True
    emprunt.date_retour = timezone.now()
    emprunt.save()

    # Mettre à jour le nombre d'exemplaires disponibles
    emprunt.livre.exemplaires_disponibles += 1
    emprunt.livre.save()

    return redirect('mes_livres_empruntes')

