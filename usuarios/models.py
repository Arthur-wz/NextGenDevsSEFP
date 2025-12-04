from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    turma = models.CharField(max_length=50)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    cartao_sus = models.CharField(max_length=20, blank=True, null=True)
    telefone_responsaveis = models.CharField(max_length=200, blank=True, null=True)
    tem_deficiencia = models.BooleanField(default=False)
    deficiencia_descricao = models.CharField(max_length=200, blank=True, null=True)
    restricao_alimentar = models.BooleanField(default=False)
    restricao_alimentar_descricao = models.CharField(max_length=200, blank=True, null=True)
    alergia_medicacao = models.BooleanField(default=False)
    alergia_medicacao_descricao = models.CharField(max_length=200, blank=True, null=True)
    autorizacao_ir_sozinho = models.BooleanField(default=False)
    pessoas_autorizadas_retirar = models.TextField(blank=True, null=True)
    observacoes_medicas = models.TextField(blank=True, null=True)
    

    def save(self, *args, **kwargs):
        if not self.matricula:
            ultimo = Aluno.objects.order_by('-id').first()
            proximo_id = (ultimo.id + 1) if ultimo else 1
            self.matricula = f"ALU{proximo_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # 🔹 novo campo
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    email = models.EmailField()
    disciplina = models.CharField(max_length=100)
    turmas = models.ManyToManyField('Turma', related_name='professores', blank=True)

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
    BIMESTRES = [
        (1, "1º Bimestre"),
        (2, "2º Bimestre"),
        (3, "3º Bimestre"),
        (4, "4º Bimestre"),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE, related_name='notas')
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    data_lancamento = models.DateField(auto_now_add=True)
    bimestre = models.IntegerField(choices=BIMESTRES) 

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina.nome}: {self.valor}"
    
# 🔹 MODELO DE ADVERTÊNCIAS
class Advertencia(models.Model):
    STATUS_CHOICES = [
        ('em_andamento', 'Em andamento'),
        ('finalizada', 'Finalizada'),
    ]

    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name='advertencias')
    coordenador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    motivo = models.TextField()

    # 🔹 Campos que estavam faltando:
    responsavel_presente = models.CharField(max_length=100, blank=True, null=True)
    descricao_ocorrido = models.TextField(blank=True, null=True)

    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_andamento')

    def __str__(self):
        return f"{self.aluno.nome} - {self.get_status_display()}"

class Coordenador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    setor = models.CharField(max_length=50, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.nome

    # --- NOVOS CAMPOS ---

class Secretaria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    setor = models.CharField(max_length=50, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

class Diretor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=100)
    email = models.EmailField()

    cpf = models.CharField(max_length=14, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=50, default="Direção")
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
