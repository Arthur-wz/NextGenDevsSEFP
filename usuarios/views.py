# usuarios/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import (
    Aluno, Professor, Nota, Advertencia,
    Turma, Disciplina, Secretaria, Diretor, Coordenador
)
from .forms import (
    AlunoForm, ProfessorForm, NotaForm,
    AdvertenciaForm, TurmaForm, DisciplinaForm, SecretariaForm, DiretorForm
)
from .decorators import grupo_requerido
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Prefetch
from django.contrib.auth import logout

# -----------------------------
# HOME / LOGIN
# -----------------------------
def home(request):
    return redirect('login')

def login_limpo(request):
    """
    Encerra sessão e encaminha para a view de login puro (LoginView).
    Projeto tem: path('login/', views.login_limpo, name='login')
                 path('login-puro/', auth_views.LoginView..., name='login_puro')
    """
    logout(request)
    request.session.flush()
    return redirect('login_puro')


# -----------------------------
# AUX: ajuda a obter perfil por user (robusto)
# -----------------------------
def obter_aluno_por_user(user):
    if not user or not user.is_authenticated:
        return None
    # Prioriza relação OneToOneField user, depois busca por nome/username (legado)
    aluno = Aluno.objects.filter(user=user).first()
    if not aluno:
        aluno = Aluno.objects.filter(nome__iexact=user.username).first()
    return aluno

def obter_professor_por_user(user):
    if not user or not user.is_authenticated:
        return None
    return Professor.objects.filter(user=user).first()

def obter_secretaria_por_user(user):
    if not user or not user.is_authenticated:
        return None
    return Secretaria.objects.filter(user=user).first()

def obter_diretor_por_user(user):
    if not user or not user.is_authenticated:
        return None
    return Diretor.objects.filter(user=user).first()


# -----------------------------
# ALUNO
# -----------------------------
@login_required(login_url='login')
@grupo_requerido("Aluno")
def aluno(request):
    aluno = obter_aluno_por_user(request.user)
    if not aluno:
        messages.error(request, "Aluno não encontrado. Contate a Secretaria.")
        # Renderiza com placeholders para evitar erros no template
        return render(request, 'aluno.html', {
            'aluno': None,
            'boletim': {},
            'disciplinas': [],
        })

    disciplinas = Disciplina.objects.filter(turmas__alunos=aluno).distinct()
    notas = Nota.objects.filter(aluno=aluno).select_related('disciplina')

    # montar boletim (disciplina -> bimestres)
    boletim = {}
    for disc in disciplinas:
        boletim[disc] = {1: None, 2: None, 3: None, 4: None}

    for nota in notas:
        if nota.disciplina in boletim:
            boletim[nota.disciplina][nota.bimestre] = nota.valor

    return render(request, 'aluno.html', {
        'aluno': aluno,
        'disciplinas': disciplinas,
        'boletim': boletim,
    })


# -----------------------------
# PROFESSOR
# -----------------------------
@login_required(login_url='login')
@grupo_requerido("Professor")
def professor(request):
    professor = obter_professor_por_user(request.user)
    if not professor:
        messages.error(request, "Professor não encontrado. Contate o administrador.")
        return redirect('login')

    disciplinas_prof = Disciplina.objects.filter(professor=professor)
    if not disciplinas_prof.exists():
        messages.warning(request, "Nenhuma disciplina atribuída. Contate a Coordenação.")
        # ainda renderiza a página, mas sem dados sensíveis
    turmas = Turma.objects.filter(disciplinas__in=disciplinas_prof).distinct()
    alunos = Aluno.objects.filter(turmas__in=turmas).distinct()

    notas = Nota.objects.filter(disciplina__in=disciplinas_prof, aluno__in=alunos)\
                        .select_related('aluno', 'disciplina')

    advertencias = Advertencia.objects.filter(aluno__in=alunos)

    # Form de lançar nota — restringe aluno ao conjunto do professor
    form = NotaForm()
    if 'aluno' in form.fields:
        form.fields['aluno'].queryset = alunos

    if request.method == 'POST':
        form = NotaForm(request.POST)
        if 'aluno' in form.fields:
            form.fields['aluno'].queryset = alunos
        if form.is_valid():
            nota_obj = form.save(commit=False)
            # comportamento: se professor tem múltiplas disciplinas talvez precise escolher,
            # por enquanto atribuímos a primeira disciplina do professor.
            disciplina_default = disciplinas_prof.first()
            if not disciplina_default:
                messages.error(request, "Você não possui disciplina cadastrada. Não é possível lançar nota.")
                return redirect('usuarios:professor')

            if nota_obj.aluno not in alunos:
                messages.error(request, "Aluno inválido para suas turmas.")
                return redirect('usuarios:professor')

            nota_obj.disciplina = disciplina_default
            nota_obj.save()
            messages.success(request, "Nota lançada com sucesso.")
            return redirect('usuarios:professor')
        else:
            if 'aluno' in form.fields:
                form.fields['aluno'].queryset = alunos

    return render(request, 'professor.html', {
        'professor': professor,
        'turmas': turmas,
        'alunos': alunos,
        'notas': notas,
        'advertencias': advertencias,
        'form': form,
    })


# -----------------------------
# EDITAR / DELETAR NOTA (Professor only)
# -----------------------------
@login_required(login_url='login')
@grupo_requerido("Professor")
def editar_nota(request, nota_id):
    professor = obter_professor_por_user(request.user)
    nota = get_object_or_404(Nota, id=nota_id)

    if nota.disciplina.professor != professor:
        messages.error(request, "Você não tem permissão para editar essa nota.")
        return redirect('usuarios:professor')

    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        # restringe alunos ao contexto do professor
        turmas = Turma.objects.filter(disciplinas__professor=professor)
        alunos = Aluno.objects.filter(turmas__in=turmas).distinct()
        if 'aluno' in form.fields:
            form.fields['aluno'].queryset = alunos
        if form.is_valid():
            form.save()
            messages.success(request, "Nota atualizada!")
            return redirect('usuarios:professor')
    else:
        form = NotaForm(instance=nota)
        turmas = Turma.objects.filter(disciplinas__professor=professor)
        alunos = Aluno.objects.filter(turmas__in=turmas).distinct()
        if 'aluno' in form.fields:
            form.fields['aluno'].queryset = alunos

    return render(request, 'editar_nota.html', {'form': form, 'nota': nota})


@login_required(login_url='login')
@grupo_requerido("Professor")
def deletar_nota(request, nota_id):
    professor = obter_professor_por_user(request.user)
    nota = get_object_or_404(Nota, id=nota_id)

    if nota.disciplina.professor != professor:
        messages.error(request, "Você não tem permissão para excluir essa nota.")
        return redirect('usuarios:professor')

    if request.method == 'POST':
        nota.delete()
        messages.success(request, "Nota excluída!")
        return redirect('usuarios:professor')

    # Se template usar GET, pede confirmação (template confirm_delete.html)
    return render(request, 'confirm_delete.html', {'obj': nota, 'tipo': 'Nota'})


# -----------------------------
# SECRETARIA (única página com blocos CRUD)
# -----------------------------
@login_required(login_url='login')
@grupo_requerido("Secretaria")
def secretaria(request):
    secretaria = obter_secretaria_por_user(request.user)
    if not secretaria:
        # cria registro mínimo se não existir para evitar erro no template
        secretaria = Secretaria.objects.create(
            user=request.user,
            nome=request.user.get_full_name() or request.user.username,
            email=request.user.email
        )

    # Fornece forms/listas para o template que possui os blocos (CRUD)
    alunos = Aluno.objects.all()
    professores = Professor.objects.all()
    disciplinas = Disciplina.objects.all()

    return render(request, 'secretaria.html', {
        'secretaria': secretaria,
        'alunos': alunos,
        'professores': professores,
        'disciplinas': disciplinas,
        # forms serão carregados via modal/abas no template quando necessário
    })


# -----------------------------
# CRUD ALUNOS (Secretaria)
# -----------------------------
@grupo_requerido("Secretaria")
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            username = slugify(aluno.nome).replace('-', '_')
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            password = "Al123456#"
            user = User.objects.create_user(username=username, password=password, email=aluno.email or "")
            try:
                grupo_aluno = Group.objects.get(name="Aluno")
                user.groups.add(grupo_aluno)
            except Group.DoesNotExist:
                pass
            aluno.user = user
            aluno.save()
            messages.success(request, f"Aluno '{aluno.nome}' cadastrado! Login: {username}")
            return redirect('usuarios:listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'cadastrar_aluno.html', {'form': form})


@grupo_requerido("Secretaria")
def listar_alunos(request):
    termo = request.GET.get('q', '')
    alunos = Aluno.objects.filter(nome__icontains=termo) if termo else Aluno.objects.all()
    return render(request, 'listar_alunos.html', {'alunos': alunos, 'termo': termo})


@grupo_requerido("Secretaria")
def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, "Aluno atualizado!")
            return redirect('usuarios:listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'editar_aluno.html', {'form': form, 'aluno': aluno})


@grupo_requerido("Secretaria")
def deletar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, "Aluno excluído!")
        return redirect('usuarios:listar_alunos')
    return render(request, 'confirm_delete.html', {'obj': aluno, 'tipo': 'Aluno'})


# -----------------------------
# CRUD PROFESSORES (Secretaria / Coordenação tem acesso visual)
# -----------------------------
@grupo_requerido("Secretaria")
def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save(commit=False)
            username = slugify(professor.nome).replace('-', '_')
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            password = "Pr123456#"
            user = User.objects.create_user(username=username, password=password, email=professor.email or "")
            try:
                grupo = Group.objects.get(name="Professor")
                user.groups.add(grupo)
            except Group.DoesNotExist:
                pass
            professor.user = user
            professor.save()
            messages.success(request, "Professor cadastrado!")
            return redirect('usuarios:listar_professores')
    else:
        form = ProfessorForm()
    return render(request, 'cadastrar_professor.html', {'form': form})


@grupo_requerido("Secretaria")
def listar_professores(request):
    termo = request.GET.get('q', '')
    professores = Professor.objects.filter(nome__icontains=termo) if termo else Professor.objects.all()
    return render(request, 'listar_professor.html', {'professores': professores, 'termo': termo})


@grupo_requerido("Secretaria")
def editar_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, "Professor atualizado!")
            return redirect('usuarios:listar_professores')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'editar_professor.html', {'form': form, 'professor': professor})


@grupo_requerido("Secretaria")
def deletar_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    if request.method == 'POST':
        professor.delete()
        messages.success(request, "Professor excluído!")
        return redirect('usuarios:listar_professores')
    return render(request, 'confirm_delete.html', {'obj': professor, 'tipo': 'Professor'})


# -----------------------------
# ADVERTÊNCIAS (Coordenação)
# -----------------------------
@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def editar_advertencia(request, id):
    advertencia = get_object_or_404(Advertencia, id=id)
    if request.method == 'POST':
        form = AdvertenciaForm(request.POST, instance=advertencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Advertência atualizada!")
            return redirect('usuarios:coordenacao')
    else:
        form = AdvertenciaForm(instance=advertencia)
    return render(request, 'editar_advertencia.html', {'form': form, 'advertencia': advertencia})


@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def deletar_advertencia(request, id):
    advertencia = get_object_or_404(Advertencia, id=id)
    if request.method == 'POST':
        advertencia.delete()
        messages.success(request, "Advertência excluída!")
        return redirect('usuarios:coordenacao')
    return render(request, 'confirm_delete.html', {'obj': advertencia, 'tipo': 'Advertência'})


# -----------------------------
# TURMAS / DISCIPLINAS (Coordenação)
# -----------------------------
@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def cadastrar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, "Turma criada!")
            return redirect('usuarios:painel_admin_coordenacao')
    else:
        form = TurmaForm()
    return render(request, 'cadastrar_turma.html', {'form': form})


@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def editar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada!")
            return redirect('usuarios:painel_admin_coordenacao')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'editar_turma.html', {'form': form, 'turma': turma})


@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def deletar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, "Turma excluída!")
        return redirect('usuarios:painel_admin_coordenacao')
    return render(request, 'confirm_delete.html', {'obj': turma, 'tipo': 'Turma'})


@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina criada!")
            return redirect('usuarios:painel_admin_coordenacao')
    else:
        form = DisciplinaForm()
    return render(request, 'cadastrar_disciplina.html', {'form': form})


@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def editar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina atualizada!")
            return redirect('usuarios:painel_admin_coordenacao')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'editar_disciplina.html', {'form': form, 'disciplina': disciplina})


@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def deletar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)
    if request.method == 'POST':
        disciplina.delete()
        messages.success(request, "Disciplina excluída!")
        return redirect('usuarios:painel_admin_coordenacao')
    return render(request, 'confirm_delete.html', {'obj': disciplina, 'tipo': 'Disciplina'})


# -----------------------------
# PAINÉIS
# -----------------------------
@login_required(login_url='login')
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
    # coordenador pode ter um perfil model Coordenador ou só usar request.user
    coordenador = Coordenador.objects.filter(user=request.user).first()
    return render(request, 'painel_admin_coordenacao.html', {
        'turmas': turmas,
        'professores': professores,
        'alunos': alunos,
        'disciplinas': disciplinas,
        'advertencias': advertencias,
        'notas': notas,
        'coordenador': coordenador,
    })


@login_required(login_url='login')
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


# -----------------------------
# COORDENAÇÃO / DIREÇÃO (aliases)
# -----------------------------
@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def coordenacao(request):
    # exibe a página de coordenação (form + lista) — manter mesmo nome de template
    # redireciona para painel administrativo quando necessário
    return redirect('usuarios:painel_admin_coordenacao')


@login_required(login_url='login')
@grupo_requerido("Direcao")
def direcao(request):
    diretor = obter_diretor_por_user(request.user)
    if not diretor:
        diretor = Diretor.objects.create(
            user=request.user,
            nome=request.user.get_full_name() or request.user.username,
            email=request.user.email
        )

    professores = Professor.objects.all()
    alunos = Aluno.objects.all()
    disciplinas = Disciplina.objects.all()
    turmas = Turma.objects.all()
    notas = Nota.objects.all()
    advertencias = Advertencia.objects.all()

    return render(request, 'direcao.html', {
        'diretor': diretor,
        'professores': professores,
        'alunos': alunos,
        'disciplinas': disciplinas,
        'turmas': turmas,
        'notas': notas,
        'advertencias': advertencias,
        'form': DiretorForm(instance=diretor),
    })


@login_required(login_url='login')
@grupo_requerido("Direcao")
def editar_diretor(request):
    diretor = obter_diretor_por_user(request.user)
    if not diretor:
        messages.error(request, "Diretor não encontrado.")
        return redirect('usuarios:direcao')
    if request.method == 'POST':
        form = DiretorForm(request.POST, instance=diretor)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas com sucesso!")
            return redirect('usuarios:direcao')
    else:
        form = DiretorForm(instance=diretor)
    return render(request, 'editar_diretor.html', {'form': form, 'diretor': diretor})


# -----------------------------
# REDIRECIONAMENTO APÓS LOGIN (Login redirect view)
# -----------------------------
def redirecionar_usuario(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    grupo = user.groups.first()
    if not grupo:
        messages.error(request, "Nenhum grupo associado ao usuário. Contate a administração.")
        return redirect('login')

    nome = grupo.name
    mapping = {
        "Aluno": "usuarios:aluno",
        "Professor": "usuarios:professor",
        "Secretaria": "usuarios:secretaria",
        "Coordenacao": "usuarios:coordenacao",
        "Direcao": "usuarios:direcao",
    }
    alvo = mapping.get(nome)
    if alvo:
        return redirect(alvo)
    return redirect('login')
