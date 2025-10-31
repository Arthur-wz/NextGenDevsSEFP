from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # 🔹 novo campo
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    turma = models.CharField(max_length=50)
    data_nascimento = models.DateField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.matricula:  # Só gera se estiver vazio
            ultimo = Aluno.objects.order_by('-id').first()
            proximo_id = (ultimo.id + 1) if ultimo else 1
            self.matricula = f"ALU{proximo_id:03d}"  # Ex: ALU001, ALU002, ...
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # 🔹 novo campo
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    email = models.EmailField()
    disciplina = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.matricula:  # Gera matrícula automática
            ultimo = Professor.objects.order_by('-id').first()
            proximo_id = (ultimo.id + 1) if ultimo else 1
            self.matricula = f"PROF{proximo_id:03d}"  # Ex: PROF001, PROF002...
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

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
    
class Nota(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True)
    disciplina = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    data_lancamento = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina}: {self.valor}"
