from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name = 'register' ),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]