# Generated by Django 5.1.5 on 2025-01-24 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('auteur', models.CharField(max_length=200)),
                ('annee_publication', models.PositiveIntegerField()),
                ('exemplaires_disponibles', models.PositiveIntegerField()),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='livres', to='bibliotheque.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Historique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateField()),
                ('date_retour', models.DateField()),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historique', to=settings.AUTH_USER_MODEL)),
                ('livre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historique', to='bibliotheque.livre')),
            ],
        ),
        migrations.CreateModel(
            name='Emprunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateField(auto_now_add=True)),
                ('date_retour', models.DateField(blank=True, null=True)),
                ('retourne', models.BooleanField(default=False)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprunts', to=settings.AUTH_USER_MODEL)),
                ('livre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprunts', to='bibliotheque.livre')),
            ],
        ),
    ]
