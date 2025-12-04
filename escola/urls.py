from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from usuarios import views
from django.contrib.auth import views as auth_views

# Página inicial → manda para login puro
def home(request):
    return redirect('login_puro')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página inicial
    path('', home, name='home'),

    # Login LIMPO → encerra sessões e redireciona para login puro
    path('login/', views.login_limpo, name='login'),

    # Login oficial
    path(
        'login-puro/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login_puro'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login_puro'),
        name='logout'
    ),

    # Para onde mandar o usuário após login
    path('redirecionar/', views.redirecionar_usuario, name='redirecionar'),

    # TODAS AS ROTAS DO SISTEMA (aluno, prof, sec, coord, direcao)
    path('usuarios/', include('usuarios.urls')),
]
