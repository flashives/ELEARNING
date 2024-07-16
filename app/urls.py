from django.urls import path
from . import views
from Utilisateurs.views import register, connexion

urlpatterns = [
    path('', register, name='register'),
    path('home/', views.home, name='home'),
    path('cours/', views.matiere, name='cours' ),
    path('cours_niveau<str:mat>/', views.lesson, name='lesson'),
    path('lesson/<str:id>/', views.lesson_detail, name='lesson_detail'),
    path('quiz/<slug:less_id>/', views.quiz, name='quiz'),
    path('changer-niveau/', views.changer_niveau, name='changer_niveau'),
    path('edit_user_info/', views.edit_user_info, name='edit_user_info'),
    path('update_user_info/', views.update_user_info, name='update_user_info'),
    path('ajout_matiere/', views.ajout_matiere, name='ajout_matiere'),
    path('ajout_lecon/', views.ajout_lecon, name='ajout_lecon'),
    path('modifier_matiere/<slug:matiere_id>', views.modifier_matiere, name='modifier_matiere'),
    path('modifier_lecon/<slug:lecon_id>', views.modifier_lecon, name='modifier_lecon'),
]