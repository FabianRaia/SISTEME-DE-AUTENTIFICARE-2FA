from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auth_app.urls")),  # Trebuie să fie inclus aici!
]
