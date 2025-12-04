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
    # PÁGINAS PRINCIPAIS (PAINÉIS)
    # =============================
    path('aluno/', views.aluno, name='aluno'),
    path('professor/', views.professor, name='professor'),
    path('secretaria/', views.secretaria, name='secretaria'),
    path('coordenacao/', views.coordenacao, name='coordenacao'),
    path('direcao/', views.direcao, name='direcao'),

    # =============================
    # CRUD — SECRETARIA
    # =============================
    path('secretaria/alunos/', views.listar_alunos, name='listar_alunos'),
    path('secretaria/aluno/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/aluno/editar/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('secretaria/aluno/deletar/<int:id>/', views.deletar_aluno, name='deletar_aluno'),

    path('secretaria/professores/', views.listar_professores, name='listar_professores'),
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

    path('coordenacao/advertencia/cadastrar/', views.cadastrar_advertencia, name='cadastrar_advertencia'),
    path('coordenacao/advertencia/editar/<int:id>/', views.editar_advertencia, name='editar_advertencia'),
    path('coordenacao/advertencia/deletar/<int:id>/', views.deletar_advertencia, name='deletar_advertencia'),

    path('coordenacao/editar/<int:coordenador_id>/', views.editar_coordenador, name='editar_coordenador'),

    # =============================
    # CRUD — PROFESSOR (NOTAS)
    # =============================
    path('professor/nota/editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('professor/nota/deletar/<int:nota_id>/', views.deletar_nota, name='deletar_nota'),

    # =============================
    # CRUD — DIREÇÃO (SUPER-PAINEL)
    # =============================
    # Alunos
    path('direcao/alunos/', views.listar_alunos, name='direcao_listar_alunos'),
    path('direcao/aluno/cadastrar/', views.cadastrar_aluno, name='direcao_cadastrar_aluno'),
    path('direcao/aluno/editar/<int:id>/', views.editar_aluno, name='direcao_editar_aluno'),
    path('direcao/aluno/deletar/<int:id>/', views.deletar_aluno, name='direcao_deletar_aluno'),

    # Professores
    path('direcao/professores/', views.listar_professores, name='direcao_listar_professores'),
    path('direcao/professor/cadastrar/', views.cadastrar_professor, name='direcao_cadastrar_professor'),
    path('direcao/professor/editar/<int:id>/', views.editar_professor, name='direcao_editar_professor'),
    path('direcao/professor/deletar/<int:id>/', views.deletar_professor, name='direcao_deletar_professor'),

    # Disciplinas
    path('direcao/disciplina/cadastrar/', views.cadastrar_disciplina, name='direcao_cadastrar_disciplina'),
    path('direcao/disciplina/editar/<int:id>/', views.editar_disciplina, name='direcao_editar_disciplina'),
    path('direcao/disciplina/deletar/<int:id>/', views.deletar_disciplina, name='direcao_deletar_disciplina'),

    # Turmas
    path('direcao/turma/cadastrar/', views.cadastrar_turma, name='direcao_cadastrar_turma'),
    path('direcao/turma/editar/<int:id>/', views.editar_turma, name='direcao_editar_turma'),
    path('direcao/turma/deletar/<int:id>/', views.deletar_turma, name='direcao_deletar_turma'),

    # Advertências
    path('direcao/advertencia/cadastrar/', views.cadastrar_advertencia, name='cadastrar_advertencia'),
    path('direcao/advertencia/editar/<int:id>/', views.editar_advertencia, name='direcao_editar_advertencia'),
    path('direcao/advertencia/deletar/<int:id>/', views.deletar_advertencia, name='direcao_deletar_advertencia'),

    # Notas
    path('direcao/nota/editar/<int:nota_id>/', views.editar_nota, name='direcao_editar_nota'),
    path('direcao/nota/deletar/<int:nota_id>/', views.deletar_nota, name='direcao_deletar_nota'),

    # Editar diretor
    path('direcao/editar/', views.editar_diretor, name='editar_diretor'),
]
