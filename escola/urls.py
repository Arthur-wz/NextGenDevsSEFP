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
from django.urls import path, include
from django.shortcuts import redirect
from usuarios import views
from django.contrib.auth import views as auth_views


# 👇 Função para redirecionar a raiz (/) direto pro login
def redirecionar_para_login(request):
    return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 Página inicial vai direto para o login
    path('', redirecionar_para_login, name='home'),

    # 👇 Rotas de login/logout padrão do Django
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 👇 Painéis de cada grupo
    path('aluno/', views.aluno, name='aluno'),
    path('professor/', views.professor, name='professor'),
    path('secretaria/', views.secretaria, name='secretaria'),
    path('coordenacao/', views.coordenacao, name='coordenacao'),
    path('direcao/', views.direcao, name='direcao'),

    # 👇 Rota que redireciona o usuário após o login (baseado no grupo)
    path('redirecionar/', views.redirecionar_usuario, name='redirecionar'),

    # 👇 Inclui outras rotas do app “usuarios” (caso tenha mais páginas depois)
    path('usuarios/', include('usuarios.urls')),
]
