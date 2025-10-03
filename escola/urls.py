"""
URL configuration for escola project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from usuarios import views
from django.contrib.auth import views as auth_views
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # página inicial
    path('aluno/', views.aluno, name='aluno'),
    path('professor/', views.professor, name='professor'),
    path('secretaria/', views.secretaria, name='secretaria'),
    path('coordenacao/', views.coordenacao, name='coordenacao'),
    path('direcao/', views.direcao, name='direcao'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('redirecionar/', views.redirecionar_usuario, name='redirecionar'),
]
