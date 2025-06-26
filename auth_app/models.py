from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta, timezone

class OTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)  # Salvează timpul generării OTP

    def is_valid(self):
        """Verifică dacă OTP-ul este valid (nu a expirat)"""
        return datetime.now(timezone.utc) - self.created_at < timedelta(minutes=5)

    @staticmethod
    def generate_otp():
        """Generează un OTP aleator de 6 cifre"""
        return str(random.randint(100000, 999999))
