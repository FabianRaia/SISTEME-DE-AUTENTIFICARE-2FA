# delete_user.py
import os
import django

# Setăm configurația Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth.models import User

username_to_delete = "Fabi"  # 🔁 modifică dacă vrei alt user

try:
    user = User.objects.get(username=username_to_delete)
    user.delete()
    print(f"[✔] Utilizatorul '{username_to_delete}' a fost șters cu succes.")
except User.DoesNotExist:
    print(f"[!] Utilizatorul '{username_to_delete}' nu există.")
