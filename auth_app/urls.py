from django.urls import path
from .views import (
    register_view, login_view, verify_otp, logout_view, home_view,
    password_reset_request_view, password_reset_verify_view, password_reset_form_view
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("verify_otp/", verify_otp, name="verify_otp"),
    path("logout/", logout_view, name="logout"),
    path("", home_view, name="home"),
    
    # Rutele pentru resetarea parolei
    path("password_reset_request/", password_reset_request_view, name="password_reset_request"),
    path("password_reset_verify/", password_reset_verify_view, name="password_reset_verify"),
    path("password_reset_form/", password_reset_form_view, name="password_reset_form"),
]
