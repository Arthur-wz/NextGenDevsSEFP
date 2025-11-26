from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from usuarios import views
from django.contrib.auth import views as auth_views

def redirecionar_para_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página inicial -> login
    path('', redirecionar_para_login, name='home'),

    # Login
    path('login/', views.login_limpo, name='login'),
    path('login-puro/', auth_views.LoginView.as_view(template_name='login.html'), name='login_puro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Redirecionamento após login
    path('redirecionar/', views.redirecionar_usuario, name='redirecionar'),

    # TODAS AS OUTRAS URLs (aluno, professor, coordenação etc)
    path('', include('usuarios.urls')),
]
