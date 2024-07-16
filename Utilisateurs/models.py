from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import *


# Create your models here.
class utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # La liaison OneToOne vers le modèle User

    class TypeChoice(models.TextChoices):
        enseignant = 'enseignant', 'enseignant'
        eleve = 'eleve', 'eleve'
    
    type = models.CharField(
        max_length=20,
        choices=TypeChoice.choices,
        default= TypeChoice.eleve
    )
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, null=True)
    moyenne = models.FloatField(default=0.0)
    notes = models.IntegerField(default=0)
    quiz_complets = models.ManyToManyField(Quiz, null=True, related_name='quiz_complets')

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_utilisateur(sender, instance, created, **kwargs):
    if created:
        utilisateur.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_utilisateur(sender,instance,**kwargs):
    instance.utilisateur.save()
