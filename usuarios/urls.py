from django.contrib import admin
from django.urls import path
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login & Home
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),

    # Aluno
    path('aluno/', views.aluno, name='aluno'),

    # Professor
    path('professor/', views.professor, name='professor'),
    path('nota/editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('nota/deletar/<int:nota_id>/', views.deletar_nota, name='deletar_nota'),

    # Secretaria
    path('secretaria/', views.secretaria, name='secretaria'),
    path('aluno/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('aluno/listar/', views.listar_alunos, name='listar_alunos'),
    path('aluno/editar/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('aluno/deletar/<int:id>/', views.deletar_aluno, name='deletar_aluno'),

    path('professor/cadastrar/', views.cadastrar_professor, name='cadastrar_professor'),
    path('professor/listar/', views.listar_professores, name='listar_professores'),
    path('professor/editar/<int:id>/', views.editar_professor, name='editar_professor'),
    path('professor/deletar/<int:id>/', views.deletar_professor, name='deletar_professor'),

    # Coordenação
    path('coordenacao/', views.painel_administrativo_coordenacao, name='painel_admin_coordenacao'),
    path('advertencia/editar/<int:id>/', views.editar_advertencia, name='editar_advertencia'),
    path('advertencia/deletar/<int:id>/', views.deletar_advertencia, name='deletar_advertencia'),

    path('turma/cadastrar/', views.cadastrar_turma, name='cadastrar_turma'),
    path('turma/editar/<int:id>/', views.editar_turma, name='editar_turma'),
    path('turma/deletar/<int:id>/', views.deletar_turma, name='deletar_turma'),

    path('disciplina/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('disciplina/editar/<int:id>/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplina/deletar/<int:id>/', views.deletar_disciplina, name='deletar_disciplina'),

    # Direção (ÚNICO PAINEL)
    path('direcao/painel/', views.painel_administrativo_direcao, name='painel_admin_direcao'),
]
