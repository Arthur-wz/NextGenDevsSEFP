from django import forms
from .models import Aluno, Professor, Disciplina, Turma, Nota, Advertencia, Secretaria, Diretor, Coordenador

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'nome', 'email', 'turma', 'data_nascimento',
            'cpf', 'cartao_sus', 'telefone_responsaveis',
            'tem_deficiencia', 'deficiencia_descricao',
            'restricao_alimentar', 'restricao_alimentar_descricao',
            'alergia_medicacao', 'alergia_medicacao_descricao',
            'autorizacao_ir_sozinho',
            'pessoas_autorizadas_retirar',
            'observacoes_medicas',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'pessoas_autorizadas_retirar': forms.Textarea(attrs={'rows': 3}),
        }

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'email','matricula', 'turmas']
        widgets = {
            'turmas': forms.CheckboxSelectMultiple(),
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['aluno', 'valor', 'bimestre', 'disciplina']
        widgets = {
            'bimestre': forms.Select(),
        }

class AdvertenciaForm(forms.ModelForm):
    class Meta:
        model = Advertencia
        fields = [
            'aluno',
            'motivo',
            'responsavel_presente',
            'descricao_ocorrido',
            'status'
        ]


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'alunos', 'disciplinas']
        widgets = {
            'alunos': forms.CheckboxSelectMultiple(),
            'disciplinas': forms.CheckboxSelectMultiple(),
        }


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'professor']

class SecretariaForm(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ['nome', 'email', 'telefone', 'cargo', 'observacoes', 'cpf']

class DiretorForm(forms.ModelForm):
    class Meta:
        model = Diretor
        fields = ['nome', 'email', 'telefone', 'cargo', 'observacoes', 'cpf']

class coordenadorForm(forms.ModelForm):
    class Meta:
        model = Coordenador
        fields = ['nome', 'email', 'telefone', 'setor', 'observacoes']
