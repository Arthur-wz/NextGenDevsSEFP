from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.utils.text import slugify

from .models import (
    Aluno, Professor, Nota, Advertencia,
    Turma, Disciplina, Secretaria, Diretor, Coordenador
)

from .forms import (
    AlunoForm, ProfessorForm, NotaForm,
    AdvertenciaForm, TurmaForm, DisciplinaForm,
    SecretariaForm, DiretorForm, coordenadorForm
)

from .decorators import grupo_requerido


# =====================================================
# HELPERS
# =====================================================

def obter_aluno_por_user(user):
    if not user.is_authenticated:
        return None
    aluno = Aluno.objects.filter(user=user).first()
    if not aluno:
        aluno = Aluno.objects.filter(nome__iexact=user.username).first()
    return aluno

def obter_professor_por_user(user):
    if not user.is_authenticated:
        return None
    return Professor.objects.filter(user=user).first()

def obter_secretaria_por_user(user):
    if not user.is_authenticated:
        return None
    return Secretaria.objects.filter(user=user).first()

def obter_diretor_por_user(user):
    if not user.is_authenticated:
        return None
    return Diretor.objects.filter(user=user).first()


# =====================================================
# LOGIN / LOGOUT / REDIRECIONAMENTO
# =====================================================

def home(request):
    return redirect('login')

def login_limpo(request):
    logout(request)
    request.session.flush()
    return redirect('login_puro')

def redirecionar_usuario(request):
    if not request.user.is_authenticated:
        return redirect('login')

    grupo = request.user.groups.first()
    if not grupo:
        messages.error(request, "Usuário sem grupo.")
        return redirect("login")

    mapping = {
        "Aluno": "usuarios:aluno",
        "Professor": "usuarios:professor",
        "Secretaria": "usuarios:secretaria",
        "Coordenacao": "usuarios:coordenacao",
        "Direcao": "usuarios:direcao",
    }

    if grupo.name in mapping:
        return redirect(mapping[grupo.name])

    messages.error(request, "Grupo desconhecido.")
    return redirect('login')


# =====================================================
# PAINEL ALUNO
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Aluno")
def aluno(request):
    aluno = obter_aluno_por_user(request.user)

    if not aluno:
        return render(request, "aluno.html")

    disciplinas = Disciplina.objects.filter(turmas__alunos=aluno).distinct()
    notas_qs = Nota.objects.filter(aluno=aluno).select_related("disciplina")

    boletim = []
    for disc in disciplinas:
        notas_disc = notas_qs.filter(disciplina=disc)
        mapa = {1: None, 2: None, 3: None, 4: None}

        soma = 0
        count = 0

        for n in notas_disc:
            if n.bimestre in mapa:
                mapa[n.bimestre] = n.valor
                soma += n.valor
                count += 1

        media = round(soma / count, 2) if count else None

        boletim.append({
            'disciplina': disc,
            'notas': mapa,
            'media': media,
        })

    return render(request, "aluno.html", {
        'aluno': aluno,
        'disciplinas': disciplinas,
        'boletim': boletim,
        'advertencias': aluno.advertencias.all(),
    })


# =====================================================
# PAINEL PROFESSOR
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Professor")
def professor(request):
    prof = obter_professor_por_user(request.user)
    if not prof:
        messages.error(request, "Professor não encontrado.")
        return redirect("login")

    disciplinas = Disciplina.objects.filter(professor=prof)
    turmas = Turma.objects.filter(disciplinas__in=disciplinas).distinct()
    alunos = Aluno.objects.filter(turmas__in=turmas).distinct()

    notas = Nota.objects.filter(
        disciplina__in=disciplinas,
        aluno__in=alunos
    ).select_related("aluno", "disciplina")

    advertencias = Advertencia.objects.filter(aluno__in=alunos)

    # Formulário de lançamento de nota
    form = NotaForm()
    form.fields['aluno'].queryset = alunos

    if request.method == "POST":
        form = NotaForm(request.POST)
        form.fields['aluno'].queryset = alunos

        if form.is_valid():
            nota = form.save(commit=False)
            nota.disciplina = disciplinas.first()
            nota.save()
            messages.success(request, "Nota lançada!")
            return redirect("usuarios:professor")

    return render(request, "professor.html", {
        'professor': prof,
        'disciplinas': disciplinas,
        'turmas': turmas,
        'alunos': alunos,
        'notas': notas,
        'advertencias': advertencias,
        'form': form,
    })


# =====================================================
# EDITAR / DELETAR NOTA
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Professor")
def editar_nota(request, nota_id):
    professor = obter_professor_por_user(request.user)
    nota = get_object_or_404(Nota, id=nota_id)

    if nota.disciplina.professor != professor and "Direcao" not in request.user.groups.values_list("name", flat=True):
        messages.error(request, "Sem permissão.")
        return redirect("usuarios:professor")

    turmas = Turma.objects.filter(disciplinas__professor=nota.disciplina.professor)
    alunos = Aluno.objects.filter(turmas__in=turmas).distinct()

    if request.method == "POST":
        form = NotaForm(request.POST, instance=nota)
        form.fields['aluno'].queryset = alunos
        if form.is_valid():
            form.save()
            messages.success(request, "Nota atualizada!")
            return redirect("usuarios:professor")
    else:
        form = NotaForm(instance=nota)
        form.fields['aluno'].queryset = alunos

    return render(request, "editar_nota.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Professor")
def deletar_nota(request, nota_id):
    professor = obter_professor_por_user(request.user)
    nota = get_object_or_404(Nota, id=nota_id)

    if nota.disciplina.professor != professor and "Direcao" not in request.user.groups.values_list("name", flat=True):
        messages.error(request, "Sem permissão.")
        return redirect("usuarios:professor")

    if request.method == "POST":
        nota.delete()
        messages.success(request, "Nota excluída!")
        return redirect("usuarios:professor")

    return redirect("usuarios:professor")


# =====================================================
# PAINEL SECRETARIA
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Secretaria")
def secretaria(request):
    sec = obter_secretaria_por_user(request.user)

    if not sec:
        sec = Secretaria.objects.create(
            user=request.user,
            nome=request.user.username,
            email=request.user.email
        )

    return render(request, "secretaria.html", {
        'secretaria': sec,
        'alunos': Aluno.objects.all(),
        'professores': Professor.objects.all(),
        'disciplinas': Disciplina.objects.all(),
    })


# =====================================================
# CRUD SECRETARIA — ALUNOS
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def cadastrar_aluno(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)

            username = slugify(aluno.nome).replace("-", "_")
            base = username
            n = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{n}"
                n += 1

            user = User.objects.create_user(
                username=username,
                password="Al123456#",
                email=aluno.email or ""
            )

            try:
                user.groups.add(Group.objects.get(name="Aluno"))
            except:
                pass

            aluno.user = user
            aluno.save()

            messages.success(request, f"Aluno cadastrado! Login: {username}")
            return redirect("usuarios:listar_alunos")
    else:
        form = AlunoForm()

    return render(request, "cadastrar_aluno.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def listar_alunos(request):
    termo = request.GET.get("q", "")
    alunos = Aluno.objects.filter(nome__icontains=termo) if termo else Aluno.objects.all()
    return render(request, "listar_alunos.html", {'alunos': alunos, 'termo': termo})


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)

    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, "Aluno atualizado!")
            return redirect("usuarios:listar_alunos")
    else:
        form = AlunoForm(instance=aluno)

    return render(request, "editar_aluno.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def deletar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)

    if request.method == "POST":
        aluno.delete()
        messages.success(request, "Aluno excluído!")
        return redirect("usuarios:listar_alunos")

    return redirect("usuarios:listar_alunos")


# =====================================================
# CRUD SECRETARIA — PROFESSORES
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def cadastrar_professor(request):
    if request.method == "POST":
        form = ProfessorForm(request.POST)
        if form.is_valid():
            prof = form.save(commit=False)

            username = slugify(prof.nome).replace("-", "_")
            base = username
            n = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{n}"
                n += 1

            user = User.objects.create_user(
                username=username,
                password="Pr123456#",
                email=prof.email or ""
            )

            try:
                user.groups.add(Group.objects.get(name="Professor"))
            except:
                pass

            prof.user = user
            prof.save()

            messages.success(request, "Professor cadastrado!")
            return redirect("usuarios:listar_professores")
    else:
        form = ProfessorForm()

    return render(request, "cadastrar_professor.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def listar_professores(request):
    termo = request.GET.get("q", "")
    professores = Professor.objects.filter(nome__icontains=termo) if termo else Professor.objects.all()
    return render(request, "listar_professor.html", {
        'professores': professores,
        'termo': termo
    })


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def editar_professor(request, id):
    prof = get_object_or_404(Professor, id=id)

    if request.method == "POST":
        form = ProfessorForm(request.POST, instance=prof)
        if form.is_valid():
            form.save()
            messages.success(request, "Professor atualizado!")
            return redirect("usuarios:listar_professores")
    else:
        form = ProfessorForm(instance=prof)

    return render(request, "editar_professor.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def deletar_professor(request, id):
    prof = get_object_or_404(Professor, id=id)

    if request.method == "POST":
        prof.delete()
        messages.success(request, "Professor excluído!")
        return redirect("usuarios:listar_professores")

    return redirect("usuarios:listar_professores")


# =====================================================
# CRUD SECRETARIA — DISCIPLINAS
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def cadastrar_disciplina(request):
    if request.method == "POST":
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina criada!")
            return redirect("usuarios:secretaria")
    else:
        form = DisciplinaForm()

    return render(request, "cadastrar_disciplina.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def editar_disciplina(request, id):
    disc = get_object_or_404(Disciplina, id=id)

    if request.method == "POST":
        form = DisciplinaForm(request.POST, instance=disc)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina atualizada!")
            return redirect("usuarios:secretaria")
    else:
        form = DisciplinaForm(instance=disc)

    return render(request, "editar_disciplina.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Secretaria", "Direcao", "Coordenacao")
def deletar_disciplina(request, id):
    disc = get_object_or_404(Disciplina, id=id)

    if request.method == "POST":
        disc.delete()
        messages.success(request, "Disciplina excluída!")
        return redirect("usuarios:secretaria")

    return redirect("usuarios:secretaria")


# =====================================================
# PAINEL COORDENAÇÃO
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def coordenacao(request):
    coordenador = Coordenador.objects.filter(user=request.user).first()

    if not coordenador:
        coordenador = Coordenador.objects.create(
            user=request.user,
            nome=request.user.username,
            email=request.user.email
        )

    return render(request, "coordenacao.html", {
        'coordenador': coordenador,
        'turmas': Turma.objects.all(),
        'professores': Professor.objects.all(),
        'alunos': Aluno.objects.all(),
        'disciplinas': Disciplina.objects.all(),
        'advertencias': Advertencia.objects.all(),
        'notas': Nota.objects.all(),
    })


# =====================================================
# CRUD COORDENAÇÃO — TURMAS
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Coordenacao", "Direcao")
def cadastrar_turma(request):
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma criada!")
            return redirect("/usuarios/coordenacao/?sec=sec-turmas")
    else:
        form = TurmaForm()

    return render(request, "cadastrar_turma.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Coordenacao", "Direcao")
def editar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)

    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada!")
            return redirect("/usuarios/coordenacao/?sec=sec-turmas")
    else:
        form = TurmaForm(instance=turma)

    return render(request, "editar_turma.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Coordenacao", "Direcao")
def deletar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)

    if request.method == "POST":
        turma.delete()
        messages.success(request, "Turma excluída!")
        return redirect("/usuarios/coordenacao/?sec=sec-turmas")

    return redirect("/usuarios/coordenacao/?sec=sec-turmas")


# =====================================================
# CRUD COORDENAÇÃO — ADVERTÊNCIAS
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Coordenacao", "Direcao")
def cadastrar_advertencia(request):
    coordenador = Coordenador.objects.filter(user=request.user).first()
    if not coordenador:
        messages.error(request, "Coordenador não encontrado.")
        return redirect("usuarios:coordenacao")

    if request.method == "POST":
        form = AdvertenciaForm(request.POST)
        if form.is_valid():
            adv = form.save(commit=False)
            adv.coordenador = coordenador.user
            adv.save()
            messages.success(request, "Advertência criada!")
            return redirect("/usuarios/coordenacao/?sec=sec-advertencias")
    else:
        form = AdvertenciaForm()

    return render(request, "cadastrar_advertencia.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Coordenacao", "Direcao")
def editar_advertencia(request, id):
    adv = get_object_or_404(Advertencia, id=id)

    if request.method == "POST":
        form = AdvertenciaForm(request.POST, instance=adv)
        if form.is_valid():
            form.save()
            messages.success(request, "Advertência atualizada!")
            return redirect("/usuarios/coordenacao/?sec=sec-advertencias")
    else:
        form = AdvertenciaForm(instance=adv)

    return render(request, "editar_advertencia.html", {'form': form})


@login_required(login_url='login')
@grupo_requerido("Coordenacao", "Direcao")
def deletar_advertencia(request, id):
    adv = get_object_or_404(Advertencia, id=id)

    if request.method == "POST":
        adv.delete()
        messages.success(request, "Advertência excluída!")
        return redirect("/usuarios/coordenacao/?sec=sec-advertencias")

    return redirect("/usuarios/coordenacao/?sec=sec-advertencias")


# =====================================================
# EDITAR COORDENADOR
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Coordenacao")
def editar_coordenador(request, coordenador_id=None):
    if coordenador_id:
        coord = get_object_or_404(Coordenador, id=coordenador_id)
    else:
        coord = get_object_or_404(Coordenador, user=request.user)

    if request.method == "POST":
        form = coordenadorForm(request.POST, instance=coord)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas!")
            return redirect("/usuarios/coordenacao/?sec=sec-info")
    else:
        form = coordenadorForm(instance=coord)

    return render(request, "editar_coordenador.html", {"form": form})


# =====================================================
# PAINEL DIREÇÃO
# =====================================================

@login_required(login_url='login')
@grupo_requerido("Direcao")
def direcao(request):
    diretor = obter_diretor_por_user(request.user)

    if not diretor:
        diretor = Diretor.objects.create(
            user=request.user,
            nome=request.user.username,
            email=request.user.email
        )

    return render(request, "direcao.html", {
        'diretor': diretor,
        'professores': Professor.objects.all(),
        'alunos': Aluno.objects.all(),
        'disciplinas': Disciplina.objects.all(),
        'turmas': Turma.objects.all(),
        'notas': Nota.objects.all(),
        'advertencias': Advertencia.objects.all(),
        'form': DiretorForm(instance=diretor),
    })


@login_required(login_url='login')
@grupo_requerido("Direcao")
def editar_diretor(request):
    diretor = obter_diretor_por_user(request.user)

    if not diretor:
        messages.error(request, "Diretor não encontrado.")
        return redirect("usuarios:direcao")

    if request.method == "POST":
        form = DiretorForm(request.POST, instance=diretor)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas!")
            return redirect("usuarios:direcao")
    else:
        form = DiretorForm(instance=diretor)

    return render(request, "editar_diretor.html", {'form': form})
