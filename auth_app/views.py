from django.shortcuts import render, redirect
from django.contrib import messages  
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from .models import OTPModel
import random

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            otp = str(random.randint(100000, 999999))

            # Ștergem OTP-uri vechi ale acestui utilizator
            OTPModel.objects.filter(user=user).delete()

            # Salvăm noul OTP în baza de date
            OTPModel.objects.create(user=user, otp_code=otp, created_at=now())

            # Salvăm username-ul în sesiune pentru verificarea OTP
            request.session['username'] = user.username
            request.session.modified = True  # Asigură-te că sesiunea este salvată

            if user.email:
                send_mail(
                    "Your OTP Code",
                    f"Your OTP code is: {otp}",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.info(request, f"An OTP has been sent to your email ({user.email}).")
                return redirect("verify_otp")
            else:
                messages.error(request, "User has no email configured. Please contact support.")
                return redirect("login")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "auth_app/login.html")

    return render(request, "auth_app/login.html")

# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Generate password reset token with timestamp
def generate_reset_token():
    return {
        "token": str(random.randint(100000, 999999)),
        "timestamp": now()
    }

# Register view
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect("login")  # Redirecționează direct la login

    return render(request, "auth_app/register.html")

# Verify OTP View
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        username = request.session.get("username")

        if not username:
            messages.error(request, "Session expired. Please login again.")
            return redirect("login")

        user = User.objects.filter(username=username).first()
        if not user:
            messages.error(request, "User not found.")
            return redirect("login")

        otp_instance = OTPModel.objects.filter(user=user).last()
        if not otp_instance or otp_instance.otp_code != entered_otp:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")

        # Check OTP expiration
        if now() > otp_instance.created_at + timedelta(minutes=5):
            messages.error(request, "OTP expired. Please login again.")
            return redirect("login")

        login(request, user)
        otp_instance.delete()  # Remove OTP after successful login
        request.session.pop("username", None)
        messages.success(request, "Logged in successfully!")
        return redirect("home")

    return render(request, "auth_app/verify_otp.html")

def generate_reset_token():
    return {
        "token": str(random.randint(100000, 999999)),
        "timestamp": now()
    }

# Cerere resetare parolă
def password_reset_request_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        
        if user:
            reset_data = generate_reset_token()
            request.session['reset_token'] = reset_data['token']
            request.session['reset_timestamp'] = reset_data['timestamp'].isoformat()
            request.session['reset_email'] = email
            send_mail(
                "Password Reset Code",
                f"Your password reset code is: {reset_data['token']}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.info(request, "A password reset code has been sent to your email.")
            return redirect("password_reset_verify")
        else:
            messages.error(request, "No account found with that email.")
            return redirect("password_reset_request")
    
    return render(request, "auth_app/password_reset_request.html")

# Verificare cod resetare parolă
def password_reset_verify_view(request):
    if request.method == "POST":
        entered_token = request.POST.get("token")
        session_token = request.session.get("reset_token")
        reset_timestamp = request.session.get("reset_timestamp")
        email = request.session.get("reset_email")

        if not reset_timestamp or now() > now().fromisoformat(reset_timestamp) + timedelta(minutes=10):
            messages.error(request, "Reset token expired. Please request a new one.")
            return redirect("password_reset_request")

        if entered_token == session_token:
            return redirect("password_reset_form")
        else:
            messages.error(request, "Invalid or expired reset code.")
            return redirect("password_reset_verify")
    
    return render(request, "auth_app/password_reset_verify.html")

# Schimbare parolă
def password_reset_form_view(request):
    if request.method == "POST":
        new_password = request.POST.get("password")
        email = request.session.get("reset_email")
        
        if email:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            request.session.pop("reset_email", None)
            request.session.pop("reset_token", None)
            messages.success(request, "Your password has been reset successfully!")
            return redirect("login")
        else:
            messages.error(request, "Session expired. Please request a new reset code.")
            return redirect("password_reset_request")
    
    return render(request, "auth_app/password_reset_form.html")

# Logout View
def logout_view(request):
    logout(request)

    # Ștergem mesajele anterioare din sesiune
    storage = get_messages(request)
    for _ in storage:
        pass  

    messages.success(request, "Logged out successfully!")
    return redirect("login")

# Home View (protected page)
@login_required
def home_view(request):
    return render(request, "auth_app/home.html", {"username": request.user.username})