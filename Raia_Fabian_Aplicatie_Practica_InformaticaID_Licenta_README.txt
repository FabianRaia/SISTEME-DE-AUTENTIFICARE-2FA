README.txt
===========

Proiect: SISTEME DE AUTENTIFICARE 2FA PENTRU O APLICAȚIE WEB  
Autor: Raia Fabian  
Coordonator: Ș.l.dr.ing. Mădălin-Dorin Pop  
Facultatea de Automatică și Calculatoare, UPT  
Program: Informatica ID  
Sesiunea: iunie 2025

---

1. ADRESA REPOSITORY-ULUI
----------------------------

Proiectul este disponibil pe Git în cadrul platformei:

https://github.com/FabianRaia/SISTEME-DE-AUTENTIFICARE-2FA

Repository-ul este public.

---

2. DESCRIEREA LIVRABILELOR
----------------------------

Arhiva proiectului conține următoarele fișiere și directoare:

- `manage.py` – scriptul principal de rulare Django
- `settings.py`, `urls.py`, `asgi.py`, `wsgi.py`, `__init__.py` – fișiere de configurare pentru aplicația Django
- `auth_app/` – aplicația custom cu modele, vizualizări, rute
- `templates/` – fișiere HTML pentru interfață
- `static/`, `staticfiles/` – fișiere statice CSS/JS/imagini
- `requirements.txt` – lista completă a pachetelor Python necesare

**Fișierele binare și compilate NU sunt incluse:**
- `db.sqlite3` – fișier de bază de date SQLite (EXCLUS)
- `__pycache__/` – fișiere Python compilate (EXCLUSE)

---

3. PAȘII DE COMPILARE (Pregătirea mediului)
--------------------------------------------

1. Deschide terminalul (CMD run as administrator)
2. Instaleaza python
	winget install --id Python.Python.3.12
2. Creează un mediu virtual:
	python -m venv venv
4. Activează mediul virtual:
	venv\Scripts\activate
5. Accesare directorului proiectului:
	F:
	cd F:\Desktop\SISTEME-DE-AUTENTIFICARE-2FA-main\SISTEME-DE-AUTENTIFICARE-2FA-main (exemplu)
6. Instalează toate dependențele:
       pip install -r requirements.txt

---

4. PAȘII DE INSTALARE
-----------------------

1. Navighează în directorul proiectului:
	F:
       cd F:\Desktop\SISTEME-DE-AUTENTIFICARE-2FA-main\SISTEME-DE-AUTENTIFICARE-2FA-main (exemplu)
2. Creează baza de date:
       python manage.py makemigrations
       python manage.py migrate
3. Creează un superuser pentru autentificare în panoul de administrare:
       python manage.py createsuperuser

---

5. PAȘII DE LANSARE
----------------------

1. Pornește serverul de dezvoltare Django:
       python manage.py runserver
2. Accesează aplicația în browser:
       http://127.0.0.1:8000/register/
3. Panoul de administrare este disponibil la:
       http://127.0.0.1:8000/admin/

---

