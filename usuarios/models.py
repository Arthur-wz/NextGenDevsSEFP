from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    turma = models.CharField(max_length=50)
    data_nascimento = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.matricula})"


class Professor(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    disciplina = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} - {self.disciplina}"

# ===============================
# 🔹 NOVAS MODELS ACADÊMICAS
# ===============================

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='disciplinas')

    def __str__(self):
        return self.nome


class Turma(models.Model):
    nome = models.CharField(max_length=50)
    alunos = models.ManyToManyField(Aluno, related_name='turmas')
    disciplinas = models.ManyToManyField(Disciplina, related_name='turmas')

    def __str__(self):
        return self.nome
