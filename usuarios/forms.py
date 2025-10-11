from django import forms
from .models import Aluno, Professor

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'email', 'turma', 'data_nascimento']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'matricula', 'email', 'disciplina']
