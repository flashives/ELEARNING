from django.contrib import admin
from .models import Niveau, Matiere,  Lesson, Commentaire, Reponse, Quiz, Question, ReponseQuiz

# Register your models here.
admin.site.register(Niveau)
admin.site.register(Matiere)
admin.site.register(Lesson)
admin.site.register(Commentaire)
admin.site.register(Reponse)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(ReponseQuiz)