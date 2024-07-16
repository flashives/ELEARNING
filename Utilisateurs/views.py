from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from .models import utilisateur
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from Elearning import settings
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generate_token
from app.models import Niveau

# Create your views here.

def register(request):
    error = False
    message = " "
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        choice = request.POST['choice']
        niveau_val = request.POST['niveau']
        #print(choice)

        if password1 != password2:
            error = True
            message = "Les deux mots de passes ne corespondent pas"
        
        if User.objects.filter(username=username).exists():
            error = True
            message = " Nom d'utilisateur deja existant"
        
        context = {
            'error' :  error,
            'message' :  message
        }

        if error:
            return render(request, 'utilisateurs/register.html', context)

        if error == False:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,   
            
            )
            if not hasattr(user,'utilisateur'):
                utilisateur.objects.create(user=user) 
                if user.is_superuser:
                    user.utilisateur.type = 'enseignant'
            else:
                user.utilisateur.type = choice 

            try:
                niveau = Niveau.objects.get(niveau=niveau_val)
                user.utilisateur.niveau = niveau
            except Niveau.DoesNotExist:
                error = True
                message = "Le niveau sélectionné n'existe pas"
                context['error'] = error
                context['message'] = message
        
            user.is_active=False
            user.utilisateur.save()
            user.save()
            # profile.save()

        # -------- Message de bienvenue ------------

        sujet = 'Bienvenue sur Eleraning Ives - Siakoul'
        msg = "Bienvenu (e), " + user.username + "sur notre plateforme de E-learning\n\nNous sommes ravi de commmencer une nouvelle experience avec vous! \n\n\n"
        envoyeur = settings.EMAIL_HOST_USER
        mail_list = [user.email]
        send_mail(sujet, msg, envoyeur, mail_list, fail_silently=False)

        # -----------CONFIRMATION EMAIL -------------
        
        current_site = get_current_site(request)
        sujet_2 = 'Confirmation de compte'
        msg_2 = render_to_string('emailConfirm.html', {
            'name': user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email = EmailMessage(
            sujet_2, 
            msg_2,
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        send_mail(sujet_2, msg_2, envoyeur, mail_list, fail_silently=False)

        

        return redirect('connexion')  # Redirect to login page after successful registration
        #print(utilisateur.type)

    return render(request, 'utilisateurs/register.html')

def connexion(request):
    msg = " "
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
            #return HttpResponse("Bien Venue ! ")
            #messages.info(request, f"Vous êtes maintenant connecté en tant que {username}.")
        else:
            #message = messages.error(request, "username ou mot de passe incorrect ")
            msg ="Nom d'utilisateur ou mot de passe incorrect"
            return render(request, 'utilisateurs/connexion.html', {'msg' : msg})
    return render(request, 'utilisateurs/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('/')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active=True
        user.save()
        login(request, user)
        messages.success(request, "Votre compte a ete cree avec succes")
        return redirect('connexion')
    
    else:
        return redirect('/')


