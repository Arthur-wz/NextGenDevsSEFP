from django.urls import path
from . import views

urlpatterns = [
    # Painel da Secretaria
    path('secretaria/', views.secretaria, name='secretaria'),

    # Alunos
    path('secretaria/cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/listar_alunos/', views.listar_alunos, name='listar_alunos'),
    path('secretaria/editar_aluno/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('secretaria/deletar_aluno/<int:id>/', views.deletar_aluno, name='deletar_aluno'),
    
    # Professores
    path('secretaria/cadastrar_professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('secretaria/listar_professores/', views.listar_professores, name='listar_professores'),
    path('secretaria/editar_professor/<int:id>/', views.editar_professor, name='editar_professor'),
    path('secretaria/deletar_professor/<int:id>/', views.deletar_professor, name='deletar_professor'),
]
