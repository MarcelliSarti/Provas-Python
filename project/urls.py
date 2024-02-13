from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('provas/', include('aplicativo.urls')),
    path('admin/', admin.site.urls),
]
