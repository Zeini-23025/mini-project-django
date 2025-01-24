from django.contrib import admin
from .models import Livre, Categorie, Emprunt, Historique

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ("titre", "auteur", "genre", "annee_publication", "exemplaires_disponibles")
    search_fields = ("titre", "auteur")

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "livre", "date_emprunt", "date_retour", "retourne")
    list_filter = ("retourne", "date_emprunt")

@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "livre", "date_emprunt", "date_retour")
    search_fields = ("utilisateur__username", "livre__titre")
