from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [

    # =============================
    # LOGIN / HOME / REDIRECIONAR
    # =============================
    path('', views.home, name='home'),
    path('login_limpo/', views.login_limpo, name='login_limpo'),
    path('redirecionar/', views.redirecionar_usuario, name='redirecionar'),

    # =============================
    # PÁGINAS PRINCIPAIS (5 únicas)
    # =============================
    path('aluno/', views.aluno, name='aluno'),
    path('professor/', views.professor, name='professor'),
    path('secretaria/', views.secretaria, name='secretaria'),
    path('coordenacao/', views.coordenacao, name='coordenacao'),
    path('direcao/', views.direcao, name='direcao'),

    # =============================
    # CRUD — SECRETARIA
    # =============================
    path('secretaria/aluno/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/aluno/editar/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('secretaria/aluno/deletar/<int:id>/', views.deletar_aluno, name='deletar_aluno'),

    path('secretaria/professor/cadastrar/', views.cadastrar_professor, name='cadastrar_professor'),
    path('secretaria/professor/editar/<int:id>/', views.editar_professor, name='editar_professor'),
    path('secretaria/professor/deletar/<int:id>/', views.deletar_professor, name='deletar_professor'),

    path('secretaria/disciplina/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('secretaria/disciplina/editar/<int:id>/', views.editar_disciplina, name='editar_disciplina'),
    path('secretaria/disciplina/deletar/<int:id>/', views.deletar_disciplina, name='deletar_disciplina'),

    # =============================
    # CRUD — COORDENAÇÃO
    # =============================
    path('coordenacao/turma/cadastrar/', views.cadastrar_turma, name='cadastrar_turma'),
    path('coordenacao/turma/editar/<int:id>/', views.editar_turma, name='editar_turma'),
    path('coordenacao/turma/deletar/<int:id>/', views.deletar_turma, name='deletar_turma'),

    path('coordenacao/advertencia/editar/<int:id>/', views.editar_advertencia, name='editar_advertencia'),
    path('coordenacao/advertencia/deletar/<int:id>/', views.deletar_advertencia, name='deletar_advertencia'),

    # =============================
    # CRUD — PROFESSOR (Not as pages — modal interno)
    # =============================
    path('professor/nota/editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('professor/nota/deletar/<int:nota_id>/', views.deletar_nota, name='deletar_nota'),

    # =============================
    # DIREÇÃO
    # =============================
    path('diretor/editar/', views.editar_diretor, name='editar_diretor'),
]
