from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, Professor, Nota, Advertencia, Turma, Disciplina, Secretaria
from .forms import (
    AlunoForm, ProfessorForm, NotaForm,
    AdvertenciaForm, TurmaForm, DisciplinaForm, SecretariaForm
)
from .decorators import grupo_requerido
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Prefetch
from django.contrib.auth import logout

# =============================
# HOME
# =============================
def home(request):
    return redirect('login')

#login

def login_limpo(request):
    logout(request)            # encerra sessão anterior
    request.session.flush()    # limpa cookies/sessão
    return redirect('login_puro')

# =============================
# 🔹 ALUNO
# =============================
@login_required(login_url='/login/')
@grupo_requerido("Aluno")
def aluno(request):
    try:
        aluno = Aluno.objects.get(email=request.user.email)
    except Aluno.DoesNotExist:
        return render(request, 'aluno.html', {
            'aluno': None,
            'notas': [],
        })

    # Disciplinas das turmas do aluno
    disciplinas = Disciplina.objects.filter(turmas__alunos=aluno).distinct()

    # Todas as notas do aluno
    notas = Nota.objects.filter(aluno=aluno)

    # Montar estrutura: disciplina -> bimestre -> nota
    boletim = {}

    for disciplina in disciplinas:
        boletim[disciplina] = {1: None, 2: None, 3: None, 4: None}

    for nota in notas:
        if nota.disciplina in boletim:
            boletim[nota.disciplina][nota.bimestre] = nota.valor

    return render(request, 'aluno.html', {
        'aluno': aluno,
        'boletim': boletim,   # dicionário organizado
        'disciplinas': disciplinas,
    })

# =============================
# PROFESSOR
# =============================
@grupo_requerido("Professor")
def professor(request):
    professor = Professor.objects.filter(user=request.user).first()

    if not professor:
        messages.error(request, "Professor não encontrado.")
        return redirect('login')

    disciplinas_professor = Disciplina.objects.filter(professor=professor)
    turmas = Turma.objects.filter(disciplinas__in=disciplinas_professor).distinct()
    alunos = Aluno.objects.filter(turmas__in=turmas).distinct()
    notas = Nota.objects.filter(disciplina__in=disciplinas_professor, aluno__in=alunos)
    advertencias = Advertencia.objects.filter(aluno__in=alunos)

    # cria o form por padrão (GET)
    form = NotaForm()

    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nova_nota = form.save(commit=False)

            # se o professor tem múltiplas disciplinas, idealmente o form deveria permitir selecionar;
            # aqui usamos a primeira — ajuste futuro: permitir seleção limitada às disciplinas do professor
            disciplina_prof = disciplinas_professor.first()
            if not disciplina_prof:
                messages.error(request, "Você não possui disciplina cadastrada.")
                return redirect('professor')

            nova_nota.disciplina = disciplina_prof
            nova_nota.save()
            messages.success(request, "Nota lançada com sucesso!")
            return redirect('professor')

    return render(request, 'professor.html', {
        'professor': professor,
        'turmas': turmas,
        'alunos': alunos,
        'notas': notas,
        'advertencias': advertencias,
        'form': form
    })

# =============================
#  NOVAS FUNÇÕES: EDITAR / EXCLUIR NOTA
# =============================
@grupo_requerido("Professor")
def editar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)

    if request.method == "POST":
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, "Nota atualizada com sucesso!")
            return redirect('professor')
    else:
        form = NotaForm(instance=nota)

    return render(request, 'editar_nota.html', {
        'form': form,
        'nota': nota
    })


@grupo_requerido("Professor")
def deletar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    nota.delete()
    messages.success(request, "Nota excluída!")
    return redirect('professor')

# =============================
# SECRETARIA
# =============================
@grupo_requerido("Secretaria")
def secretaria(request):

    # procura o registro da secretaria pelo usuário conectado
    secretaria = Secretaria.objects.filter(user=request.user).first()

    # cria automaticamente caso não exista
    if not secretaria:
        secretaria = Secretaria.objects.create(
            user=request.user,
            nome=request.user.get_full_name() or request.user.username,
            email=request.user.email
        )

    return render(request, 'secretaria.html', {'secretaria': secretaria})

# =============================
# CRUD ALUNOS
# =============================
@grupo_requerido("Secretaria")
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)

            username = slugify(aluno.nome).replace('-', '_')

            if User.objects.filter(username=username).exists():
                messages.error(request, f"O login '{username}' já existe.")
                return render(request, 'cadastrar_aluno.html', {'form': form})

            password = "Al123456#"
            user = User.objects.create_user(username=username, password=password, email=aluno.email)
            user.groups.add(Group.objects.get(name="Aluno"))

            aluno.user = user
            aluno.save()

            messages.success(request, f"Aluno '{aluno.nome}' cadastrado! Login: {username}")
            return redirect('listar_alunos')
    else:
        form = AlunoForm()

    return render(request, 'cadastrar_aluno.html', {'form': form})

@grupo_requerido("Secretaria")
def listar_alunos(request):
    termo = request.GET.get('q')
    alunos = Aluno.objects.filter(nome__icontains=termo) if termo else Aluno.objects.all()
    return render(request, 'listar_alunos.html', {'alunos': alunos, 'termo': termo})

@grupo_requerido("Secretaria")
def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)

    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('listar_alunos')
    else:
        form = AlunoForm(instance=aluno)

    return render(request, 'editar_aluno.html', {'form': form, 'aluno': aluno})

@grupo_requerido("Secretaria")
def deletar_aluno(request, id):
    get_object_or_404(Aluno, id=id).delete()
    return redirect('listar_alunos')

# =============================
# CRUD PROFESSORES
# =============================
@grupo_requerido("Secretaria")
def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save(commit=False)

            username = slugify(professor.nome).replace('-', '_')

            if User.objects.filter(username=username).exists():
                messages.error(request, f"O login '{username}' já existe.")
                return render(request, 'cadastrar_professor.html', {'form': form})

            password = "Pr123456#"
            user = User.objects.create_user(username=username, password=password, email=professor.email)
            user.groups.add(Group.objects.get(name="Professor"))

            professor.user = user
            professor.save()

            messages.success(request, "Professor cadastrado!")
            return redirect('listar_professores')
    else:
        form = ProfessorForm()

    return render(request, 'cadastrar_professor.html', {'form': form})

@grupo_requerido("Secretaria")
def listar_professores(request):
    termo = request.GET.get('q')
    professores = Professor.objects.filter(nome__icontains=termo) if termo else Professor.objects.all()

    return render(request, 'listar_professor.html', {
        'professores': professores,
        'termo': termo
    })

@grupo_requerido("Secretaria")
def editar_professor(request, id):
    professor = get_object_or_404(Professor, id=id)

    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('listar_professores')
    else:
        form = ProfessorForm(instance=professor)

    return render(request, 'editar_professor.html', {'form': form, 'professor': professor})

@grupo_requerido("Secretaria")
def deletar_professor(request, id):
    get_object_or_404(Professor, id=id).delete()
    return redirect('listar_professores')

# =============================
# ADVERTÊNCIAS
# =============================
@grupo_requerido("Coordenacao")
def editar_advertencia(request, id):
    advertencia = get_object_or_404(Advertencia, id=id)

    if request.method == "POST":
        form = AdvertenciaForm(request.POST, instance=advertencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Advertência atualizada!")
            return redirect('coordenacao')
    else:
        form = AdvertenciaForm(instance=advertencia)

    return render(request, "editar_advertencia.html", {
        "form": form,
        "advertencia": advertencia
    })

@grupo_requerido("Coordenacao")
def deletar_advertencia(request, id):
    get_object_or_404(Advertencia, id=id).delete()
    messages.success(request, "Advertência excluída!")
    return redirect('coordenacao')

# =============================
# TURMAS
# =============================
@grupo_requerido("Coordenacao")
def cadastrar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma criada!")
            return redirect('painel_admin_coordenacao')
    else:
        form = TurmaForm()

    return render(request, 'cadastrar_turma.html', {'form': form})

@grupo_requerido("Coordenacao")
def editar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)

    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada!")
            return redirect('painel_admin_coordenacao')
    else:
        form = TurmaForm(instance=turma)

    return render(request, 'editar_turma.html', {'form': form, 'turma': turma})

@grupo_requerido("Coordenacao")
def deletar_turma(request, id):
    get_object_or_404(Turma, id=id).delete()
    messages.success(request, "Turma excluída!")
    return redirect('painel_admin_coordenacao')

# =============================
#DISCIPLINAS
# ============================= 
@grupo_requerido("Coordenacao")
def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina criada!")
            return redirect('painel_admin_coordenacao')
    else:
        form = DisciplinaForm()

    return render(request, 'cadastrar_disciplina.html', {'form': form})

@grupo_requerido("Coordenacao")
def editar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina atualizada!")
            return redirect('painel_admin_coordenacao')
    else:
        form = DisciplinaForm(instance=disciplina)

    return render(request, 'editar_disciplina.html', {'form': form, 'disciplina': disciplina})

@grupo_requerido("Coordenacao")
def deletar_disciplina(request, id):
    get_object_or_404(Disciplina, id=id).delete()
    messages.success(request, "Disciplina excluída!")
    return redirect('painel_admin_coordenacao')

# =============================
#PAINÉIS
# =============================
@grupo_requerido("Coordenacao")
def painel_administrativo_coordenacao(request):
    turmas = Turma.objects.prefetch_related(
        Prefetch('alunos', queryset=Aluno.objects.all()),
        Prefetch('disciplinas', queryset=Disciplina.objects.all())
    )
    professores = Professor.objects.all()
    alunos = Aluno.objects.all()
    disciplinas = Disciplina.objects.all()
    advertencias = Advertencia.objects.all()
    notas = Nota.objects.all()

    return render(request, 'painel_admin_coordenacao.html', {
        'turmas': turmas,
        'professores': professores,
        'alunos': alunos,
        'disciplinas': disciplinas,
        'advertencias': advertencias,
        'notas': notas
    })

@grupo_requerido("Direcao")
def painel_administrativo_direcao(request):
    professores = Professor.objects.all()
    alunos = Aluno.objects.all()
    advertencias = Advertencia.objects.all()
    notas = Nota.objects.all()

    return render(request, 'direcao.html', {
        'professores': professores,
        'alunos': alunos,
        'advertencias': advertencias,
        'notas': notas
    })

# =============================
#COORDENAÇÃO
# =============================
@grupo_requerido("Coordenacao")
def coordenacao(request):
    return redirect('painel_admin_coordenacao')

# =============================
#DIREÇÃO
# =============================
@grupo_requerido("Direcao")
def direcao(request):
    return redirect('painel_admin_direcao')

# =============================
# REDIRECIONAR APÓS LOGIN
# =============================
def redirecionar_usuario(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    grupo = user.groups.first()

    if not grupo:
        return redirect('login')

    if grupo.name == "Aluno":
        return redirect('aluno')

    if grupo.name == "Professor":
        return redirect('professor')

    if grupo.name == "Secretaria":
        return redirect('secretaria')

    if grupo.name == "Coordenacao":
        return redirect('coordenacao')

    if grupo.name == "Direcao":
        return redirect('direcao')

    return redirect('login')
