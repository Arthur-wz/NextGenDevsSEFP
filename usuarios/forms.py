from django import forms
from .models import Aluno, Professor, Disciplina, Turma, Nota, Advertencia, Secretaria

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
        fields = ['nome', 'email', 'disciplina']

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['aluno', 'valor', 'bimestre']

class AdvertenciaForm(forms.ModelForm):
    class Meta:
        model = Advertencia
        fields = ['aluno', 'motivo', 'status']

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
        fields = ['nome', 'email', 'telefone', 'setor', 'observacoes']
