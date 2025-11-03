from django import forms
from .models import Aluno, Professor, Disciplina, Turma, Nota

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'turma', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'email', 'disciplina']

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['aluno', 'disciplina', 'valor']
