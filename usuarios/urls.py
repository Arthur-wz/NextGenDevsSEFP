from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [

    # Painéis principais
    path('aluno/', views.aluno, name='aluno'),
    path('professor/', views.professor, name='professor'),
    path('secretaria/', views.secretaria, name='secretaria'),
    path('coordenacao/', views.coordenacao, name='coordenacao'),
    path('direcao/', views.direcao, name='direcao'),

    # Alunos
    path('aluno/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('aluno/listar/', views.listar_alunos, name='listar_alunos'),
    path('aluno/editar/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('aluno/deletar/<int:id>/', views.deletar_aluno, name='deletar_aluno'),

    # Professores
    path('professor/cadastrar/', views.cadastrar_professor, name='cadastrar_professor'),
    path('professor/listar/', views.listar_professores, name='listar_professores'),
    path('professor/editar/<int:id>/', views.editar_professor, name='editar_professor'),
    path('professor/deletar/<int:id>/', views.deletar_professor, name='deletar_professor'),

    # Notas
    path('nota/editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('nota/deletar/<int:nota_id>/', views.deletar_nota, name='deletar_nota'),

    # Advertências
    path('advertencia/editar/<int:id>/', views.editar_advertencia, name='editar_advertencia'),
    path('advertencia/deletar/<int:id>/', views.deletar_advertencia, name='deletar_advertencia'),

    # Turmas
    path('turma/cadastrar/', views.cadastrar_turma, name='cadastrar_turma'),
    path('turma/editar/<int:id>/', views.editar_turma, name='editar_turma'),
    path('turma/deletar/<int:id>/', views.deletar_turma, name='deletar_turma'),

    # Disciplinas
    path('disciplina/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('disciplina/editar/<int:id>/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplina/deletar/<int:id>/', views.deletar_disciplina, name='deletar_disciplina'),

    # Direção (editar dados)
    path('diretor/editar/', views.editar_diretor, name='editar_diretor'),

    # Painéis administrativos
    path('painel/coordenacao/', views.painel_administrativo_coordenacao, name='painel_admin_coordenacao'),
    path('painel/direcao/', views.painel_administrativo_direcao, name='painel_admin_direcao'),
]
