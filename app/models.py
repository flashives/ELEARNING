from django.db import models
from django.core.validators import FileExtensionValidator
#from Utilisateurs.models import utilisateur
from django.contrib.auth.models import User
from django.utils.text import slugify



# Create your models here.


class Niveau(models.Model):
    class NiveauChoices(models.TextChoices):
        NIVEAU_6E = '6e', '6e'
        NIVEAU_5E = '5e', '5e'
        NIVEAU_4E = '4e', '4e'
        NIVEAU_3E = '3e', '3e'
        NIVEAU_2ND_A = '2nd A', '2nd A'
        NIVEAU_2ND_C = '2nd C', '2nd C'
        NIVEAU_1RE_A = '1re A', '1re A'
        NIVEAU_1RE_D = '1re D', '1re D'
        NIVEAU_TLE_A = 'Tle A', 'Tle A'
        NIVEAU_TLE_D = 'Tle D', 'Tle D'

    niveau = models.CharField(
        max_length=10,
        choices=NiveauChoices.choices,
        default=NiveauChoices.NIVEAU_6E,
        unique=True
    )

    
    description = models.TextField()
    image = models.ImageField(upload_to='niveau_photos/',null=True, blank=True)
    
    #slug = models.SlugField(default='default-slug')

    def __str__(self):
        return self.get_niveau_display()
    
 

class Matiere(models.Model):
    nom = models.CharField(max_length=100, primary_key=True, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='matiere_photos/',null=True, blank=True)
    slug = models.SlugField(default='default-slug')
    #niveaux = models.ManyToManyField(Niveau, related_name='niveaux')

    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(['mp4', 'mpeg', 'avi'])])
    pdf = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(['pdf', 'odt', 'pptx','docx'])])
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE,null=True, related_name='lessons' ) #evaluation = models.OneToOneField(Evaluation, on_delete=models.CASCADE, null=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, null=True, related_name='niveaux')
    createur = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    slug = models.SlugField(default='default-slug')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
class Commentaire(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    nom_comm = models.CharField(max_length=100,blank=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    corps = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.nom_comm = slugify("commenter par"+ str(self.auteur) + 'a' + str(self.date))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom_comm
    
    class Meta:
        ordering = ['-date']

class Reponse(models.Model):
    nom_comm = models.ForeignKey(Commentaire, on_delete=models.CASCADE, related_name="reponses")
    corps = models.TextField(max_length=500)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ajout = models.DateField(auto_now_add=True)

    def __str__(self):
        return "reponse a" + str(self.nom_comm.nom_comm)

class Quiz(models.Model):
    titre = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    description = models.TextField()
    slug = models.SlugField(default='default-slug')

    def __str__(self):
        return self.titre.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question

class ReponseQuiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reponse = models.CharField(max_length=500)
    est_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.reponse
