from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    email = models.EmailField()
    turma = models.CharField(max_length=20)
    data_nascimento = models.DateField()

    def save(self, *args, **kwargs):
        if not self.matricula:  # Só gera se estiver vazio
            ultimo = Aluno.objects.order_by('-id').first()
            proximo_id = (ultimo.id + 1) if ultimo else 1
            self.matricula = f"ALU{proximo_id:03d}"  # Ex: ALU001, ALU002, ...
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Professor(models.Model):
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
