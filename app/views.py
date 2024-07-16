from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from Utilisateurs.models import utilisateur
from django.contrib.auth.models import User
from .models import Lesson, Commentaire, Reponse, Niveau
from django.db import transaction
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@login_required
def home(request):
    passe = False
    user = request.user
    uti = get_object_or_404(utilisateur, user=user)
    level = uti.niveau
    moyenne = uti.moyenne
    matieres = Matiere.objects.all()
    notes = uti.notes
    lessons = Lesson.objects.filter(niveau=level)
    total_lessons = lessons.count()
    if total_lessons > 0:
        moyenne = notes / total_lessons
        progress = moyenne * 100
        uti.moyenne = moyenne
        uti.save()
        if progress >= 70:
            passe = True
    else:
        moyenne = 0
        progress = 0

    return render(request, 'app/home.html', {'matieres': matieres, 'level' : level,'moyenne' : moyenne, 'progress' : progress, 'total_lessons' : total_lessons, 'passe':passe})


@login_required
def changer_niveau(request):
    user = request.user
    user_profile = get_object_or_404(utilisateur, user=user)
    current_level = user_profile.niveau.niveau

    # Define the order of levels
    if current_level == '2nd A':
        level_order = [
            '6e', '5e', '4e', '3e',
            '2nd A',  '1re A',
            'Tle A'
        ]
    elif current_level == '2nd C':
        level_order = [
            '6e', '5e', '4e', '3e',
            '2nd C',  '1re D',
            'Tle D'
        ]
    else:
        level_order = [
            '6e', '5e', '4e', '3e', '2nd A', 
            '2nd C', '1re A' ,'1re D', 'Tle A',
            'Tle D'
        ]

    try:
        current_level_index = level_order.index(current_level)
    except ValueError:
        print("Current level not found in the level order list.")
        return redirect('home')

    next_level = level_order[current_level_index + 1] if current_level_index + 1 < len(level_order) else None
    
    if next_level:
        try:
            next_level_instance = Niveau.objects.get(niveau=next_level)
        except Niveau.DoesNotExist:
            print(f"Next level '{next_level}' does not exist in the Niveau model.")
            return redirect('home')

        
        with transaction.atomic():
            user_profile.niveau = next_level_instance
            user_profile.notes = 0
            user_profile.moyenne = 0
            user_profile.quiz_complets.clear()
            user_profile.save()

    return redirect('home')

@login_required
def matiere(request):
    user = request.user
    uti = get_object_or_404(utilisateur, user=user)
    level = uti.niveau
    matieres = Matiere.objects.all()
    return render(request, 'app/courses.html', {'matieres' : matieres})

@login_required
def lesson(request, mat):
    user = request.user
    uti = get_object_or_404(utilisateur, user=user)
    level = uti.niveau
    lessons = Lesson.objects.filter(matiere = mat, niveau = uti.niveau)
    if user.is_staff:
        lessons = Lesson.objects.all()
        level = 'enseignant'
    return render(request, 'app/lessons.html', {'lessons':lessons, 'level': level, 'mat': mat })

@login_required
def lesson_detail(request, id):
    user = request.user
    uti = get_object_or_404(utilisateur, user=user)
    level = uti.niveau
    lesson = get_object_or_404(Lesson, title=id)

    # Gestion des commentaires
    if request.method == 'POST':
        if 'commentaire_id' in request.POST:
            # Réponse à un commentaire existant
            commentaire = get_object_or_404(Commentaire, id=request.POST.get('commentaire_id'))
            corps = request.POST.get('corps')
            if corps:
                Reponse.objects.create(nom_comm=commentaire, auteur=user, corps=corps)
        else:
            # Nouveau commentaire
            corps = request.POST.get('corps')
            if corps:
                Commentaire.objects.create(lesson=lesson, auteur=user, corps=corps)

        return redirect('lesson_detail', id=id)

    commentaires = Commentaire.objects.filter(lesson=lesson)

    return render(request, 'app/lesson_detail.html', {
        'lesson': lesson,
        'level': level,
        'commentaires': commentaires,
    })

def quiz(request, less_id):
    passe = False
    a_composer = False
    user = request.user
    uti = get_object_or_404(utilisateur, user=user)
    quizze = get_object_or_404(Quiz, slug=less_id)
    questions = Question.objects.filter(quiz=quizze)
    questions_with_answers = []

    if quizze in uti.quiz_complets.all():
        return HttpResponse('Vous avez dja traiter ce sujet')

    for question in questions:
        answers = ReponseQuiz.objects.filter(question=question)
        questions_with_answers.append({
            'question': question,
            'answers': answers
        })
    
    if request.method == 'POST':
        user_answers = {}
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                user_answers[question.id] = int(selected_answer_id)

        # Traitement des réponses de l'utilisateur
        # Par exemple, vérifiez les réponses correctes et calculez le score
        score = 0
        for question_id, answer_id in user_answers.items():
            answer = ReponseQuiz.objects.get(id=answer_id)
            if answer.est_correct:
                score += 1
        
        lessons = Lesson.objects.all()
        nbr_lessons = len(lessons)
        uti.quiz_complets.add(quizze)
        uti.notes += score
        uti.moyenne = uti.notes*0.7


        uti.save()

        
        
          

    return render(request, 'app/quiz.html',{'quizze': quizze,'questions' : questions, 'questions_with_answers': questions_with_answers} )


@login_required
def edit_user_info(request):
    return render(request, 'app/edit_user_info.html')

@login_required
def update_user_info(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        niveau_nom = request.POST['niveau']

        try:
            niveau = Niveau.objects.get(niveau=niveau_nom)
        except Niveau.DoesNotExist:
            # Handle the case where the niveau does not exist, e.g., return an error
            return render(request, 'app/edit_user_info.html', {
                'error': 'Niveau invalide.'
            })

        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.utilisateur.niveau = niveau
        user.save()
        user.utilisateur.save()

        return redirect('home')
    else:
        return render(request, 'app/edit_user_info.html')
    
@user_passes_test(lambda u: u.is_superuser)
def ajout_matiere(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if nom and description and image:
            Matiere.objects.create(nom=nom, description=description, image=image)
            return redirect('cours')
    
    return render(request, 'app/ajout_matiere.html')

@user_passes_test(lambda u: u.is_superuser)
def ajout_lecon(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        pdf = request.FILES.get('pdf')
        matiere_id = request.POST.get('matiere')
        niveau_id = request.POST.get('niveau')
        createur_id = request.POST.get('createur')

        matiere = Matiere.objects.get(id=matiere_id)
        niveau = Niveau.objects.get(id=niveau_id)
        createur = User.objects.get(id=createur_id)

        if title and video and pdf and matiere and niveau and createur:
            Lesson.objects.create(
                title=title,
                description=description,
                image=image,
                video=video,
                pdf=pdf,
                matiere=matiere,
                niveau=niveau,
                createur=createur
            )
            return redirect('cours')  # Ajustez selon votre URL

    context = {
        'matieres': Matiere.objects.all(),
        'niveaux': Niveau.objects.all(),
        'createurs': User.objects.all()
    }
    return render(request, 'app/ajout_lecon.html', context)

@user_passes_test(lambda u: u.is_superuser)
def modifier_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, slug=matiere_id)

    if request.method == 'POST':
        matiere.nom = request.POST.get('nom')
        matiere.description = request.POST.get('description')
        if request.FILES.get('image'):
            matiere.image = request.FILES.get('image')
        matiere.save()
        return redirect('cours')  # Ajustez selon votre URL

    context = {
        'matiere': matiere
    }
    return render(request, 'app/modifier_matiere.html', context)

@user_passes_test(lambda u: u.is_superuser)
def modifier_lecon(request, lecon_id):
    lecon = get_object_or_404(Lesson, slug=lecon_id)

    if request.method == 'POST':
        lecon.title = request.POST.get('title')
        lecon.description = request.POST.get('description')
        if request.FILES.get('image'):
            lecon.image = request.FILES.get('image')
        if request.FILES.get('video'):
            lecon.video = request.FILES.get('video')
        if request.FILES.get('pdf'):
            lecon.pdf = request.FILES.get('pdf')
        lecon.matiere.nom = request.POST.get('matiere')
        lecon.niveau.niveau = request.POST.get('niveau')
        lecon.save()
        return redirect('cours')  # Ajustez selon votre URL

    context = {
        'lecon': lecon,
        'matieres': Matiere.objects.all(),
        'niveaux': Niveau.objects.all()
    }
    return render(request, 'app/modifier_lecon.html', context)
