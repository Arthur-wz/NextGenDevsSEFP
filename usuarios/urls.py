from django.urls import path
from . import views

urlpatterns = [
    # Painel da Secretaria
    path('secretaria/', views.secretaria, name='secretaria'),

    # Alunos
    path('secretaria/cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/listar_alunos/', views.listar_alunos, name='listar_alunos'),

    # Professores
    path('secretaria/cadastrar_professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('secretaria/listar_professores/', views.listar_professores, name='listar_professores'),
]
