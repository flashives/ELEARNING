from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import utilisateur

class utilisateurInline(admin.StackedInline):
    model = utilisateur
    can_delete = False
    verbose_name_plural = 'Utilisateurs'

class UserAdmin(BaseUserAdmin):
    inlines = (utilisateurInline,)
    list_display = ('username', 'email', 'last_name', 'first_name', 'get_type')

    def get_type(self, instance):
        return instance.utilisateur.type
    get_type.short_description = 'Type'

# Personnalisation de l'admin pour le modèle Utilisateur
class UtilisateurAdmin(admin.ModelAdmin):
    filter_horizontal = ('quiz_complets',)  # Permet d'éditer quiz_complets avec une sélection multi-choix

# Désenregistrement de l'admin par défaut de User et réenregistrement avec votre personnalisation
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Enregistrement de l'admin pour le modèle Utilisateur
admin.site.register(utilisateur, UtilisateurAdmin)
