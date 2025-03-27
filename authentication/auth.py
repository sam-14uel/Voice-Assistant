from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import SignUpSerializer, UsernameSignInSerializer
from AI_Agent_Config import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import redirect

# class SignUpView(generics.CreateAPIView):
class SignUpView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']
        dob = request.POST['dob']
        

        if User.objects.filter(username=username):
            return Response({"error": f"user with Username : '{username}' already exists ! please try another username"}, status=400)

        if User.objects.filter(email=email):
            return Response({"error": f"Email : '{email}' already in use"}, status=400)
        
        if len(username)>18:
            return Response({"error": f"Username : '{username} is too long ! Must be less than 18"}, status=400)

        if pass1 != pass2:
            return Response({"error": "Passwords Do not match !"}, status=400)
        
        if len(pass1)<8:
            return Response({"error": "Passwords Must Be More than 8 characters"}, status=400)
        
        myuser = User.objects.create_user(username, email, pass1 )
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.username = username
        myuser.is_active = False
        myuser.save()
        # profile = Profile.objects.get(user=myuser)
        # profile.date_of_birth = dob
        # profile.save()

        # welcome email
        current_site = get_current_site(request)
        subject = "WELCOME TO AFRIWALLSTREET"
        message = "Hello " + myuser.first_name +"! \n" + "Welcome to AFRIWALLSTREET! \n(you are receiving this mail because an account has been created with " + myuser.email +"\n Thank you for creating an account in Afriwallstreet \n we have also sent you a mail with a link to confirm your email and activate your account \n\n Thanks once again! \n\n\n hello@afriwallstreet.com\n(Afriwallstreet Support)"
        email_1 = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        #email.fail_silently = True
        email_1.send()

        # Email address confirmation
        current_site = get_current_site(request)
        email_subject = "Verify your Email Address"
        message2 = render_to_string('auth/email_confirmation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        #email.fail_silently = True
        email.send()

        if myuser is not None:
            return Response({"success": f"You have successfully created an account with @{username} we have sent a mail to {email} to please check your inbox and confirm your email with confirmation link\nif you can't find our message you can check your spam folder note that link is valid for 15 minutes from now "}, status=200)
        
        return Response({"error": "Invalid Credentials"}, status=400)


class SignInView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UsernameSignInSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": f"Hey 👋 @{username} Welcome to Afriwallstreet", "token": token.key}, status=200)
        return Response({"error": "Invalid Credentials"}, status=400)
    

def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        # login(request, myuser)
        return JsonResponse({
            'redirect_url': '',
        })
    else:
        return JsonResponse({
            'redirect_url': '',
        })


def signout(request):
    # logout(request)
    return JsonResponse({
        'redirect_url': '',
    })


def account_login(request):
    # request_url = request.META['HTTP_REFERER']
    return JsonResponse({
        'redirect_url': '',
    })

def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({
        'exists': exists,
    })


def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({
        'exists': exists,
    })


# forgot password system
def forgot_password(request):
    if request.method == 'POST':
        my_user_email = request.POST['email']
        if User.objects.filter(email=my_user_email).exists():
            user = User.objects.get(email=my_user_email)
            current_site = get_current_site(request)
            email_subject = "Reset Password @AFRIWALLSTREET"
            message = render_to_string('auth/reset_password_email.html',{
                'user': user,
                'username': user.username,
                'name': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })
            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True # type: ignore
            email.send()
            return JsonResponse({
                'exists': "",
            })
        else:
            return JsonResponse({
            'exists': "",
        })
            return redirect('forgot_password')
    return JsonResponse({
        'exists': "",
    })