from django.db import models
from django.contrib.auth.models import User

# Modèle pour les catégories


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Modèle pour les livres


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL,
        null=True,
        related_name='livres'
        )
    annee_publication = models.PositiveIntegerField()
    exemplaires_disponibles = models.PositiveIntegerField()

    def __str__(self):
        return self.titre

# Modèle pour les emprunts


class Emprunt(models.Model):
    utilisateur = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='emprunts'
        )
    livre = models.ForeignKey(
        Livre, on_delete=models.CASCADE,
        related_name='emprunts'
        )
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True, blank=True)
    retourne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"

# Modèle pour l'historique


class Historique(models.Model):
    utilisateur = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='historique'
        )
    livre = models.ForeignKey(
        Livre, on_delete=models.CASCADE,
        related_name='historique'
        )
    date_emprunt = models.DateField()
    date_retour = models.DateField()

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"

    @staticmethod
    def ajouter_historique(emprunt):
        Historique.objects.create(
            utilisateur=emprunt.utilisateur,
            livre=emprunt.livre,
            date_emprunt=emprunt.date_emprunt,
            date_retour=emprunt.date_retour
        )
        emprunt.delete()
