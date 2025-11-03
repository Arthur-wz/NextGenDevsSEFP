from django.contrib import admin
from .models import Aluno, Professor, Disciplina, Turma, Nota

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'email', 'user', 'turmas_list')
    search_fields = ('nome', 'matricula', 'email', 'user__username')
    list_filter = ('turmas',)
    autocomplete_fields = ['user']

    fieldsets = (
        ("Informações do Aluno", {
            'fields': ('nome', 'email', 'turmas')
        }),
        ("Vínculo com Usuário", {
            'fields': ('user',)
        }),
    )

    def turmas_list(self, obj):
        return ", ".join([t.nome for t in obj.turmas.all()])
    turmas_list.short_description = 'Turmas'

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'email', 'user')
    search_fields = ('nome', 'matricula', 'email', 'user__username')
    autocomplete_fields = ['user']

    fieldsets = (
        ("Informações do Professor", {
            'fields': ('nome', 'email', 'disciplina')
        }),
        ("Vínculo com Usuário", {
            'fields': ('user',)
        }),
    )

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'professor')
    list_filter = ('professor',)
    search_fields = ('nome',)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'disciplinas_list', 'alunos_count')
    filter_horizontal = ('alunos', 'disciplinas')  # 👈 deixa os M2M mais fáceis de selecionar

    def disciplinas_list(self, obj):
        return ", ".join([d.nome for d in obj.disciplinas.all()])
    disciplinas_list.short_description = 'Disciplinas'

    def alunos_count(self, obj):
        return obj.alunos.count()
    alunos_count.short_description = 'Nº de Alunos'

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'valor', 'data_lancamento')
    list_filter = ('disciplina', 'aluno')
    search_fields = ('aluno__nome', 'disciplina__nome')