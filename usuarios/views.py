from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Aluno, Professor
from .forms import AlunoForm, ProfessorForm
from .decorators import grupo_requerido



# 🔹 Página padrão (não precisa mais ser "Seja bem-vindo", mas deixei por segurança)
def home(request):
    return redirect('login')


# 🔹 Painel do Aluno
@grupo_requerido("Aluno")
def aluno(request):
    return render(request, 'aluno.html')


# 🔹 Painel do Professor
@grupo_requerido("Professor")
def professor(request):
    return render(request, 'professor.html')


# 🔹 Painel da Secretaria
@grupo_requerido("Secretaria")
def secretaria(request):
    return render(request, 'secretaria.html')


# 🔹 Painel da Coordenação
@grupo_requerido("Coordenacao")
def coordenacao(request):
    return render(request, 'coordenacao.html')  # Corrigido o nome do HTML


# 🔹 Painel da Direção
@grupo_requerido("Direcao")
def direcao(request):
    return render(request, 'direcao.html')


# 🔹 Redireciona o usuário conforme o grupo dele
def redirecionar_usuario(request):
    if request.user.groups.filter(name="Aluno").exists():
        return redirect('aluno')
    elif request.user.groups.filter(name="Professor").exists():
        return redirect('professor')
    elif request.user.groups.filter(name="Secretaria").exists():
        return redirect('secretaria')
    elif request.user.groups.filter(name="Coordenacao").exists():
        return redirect('coordenacao')
    elif request.user.groups.filter(name="Direcao").exists():
        return redirect('direcao')
    else:
        return redirect('login')


# ===============================
# 🔹 VIEWS - Secretaria (cadastros e listagens)
# ===============================

@grupo_requerido("Secretaria")
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'cadastrar_aluno.html', {'form': form})


@grupo_requerido("Secretaria")
def listar_alunos(request): 
    alunos = Aluno.objects.all()
    return render(request, 'listar_alunos.html', {'alunos': alunos})

@grupo_requerido("Secretaria")
def editar_aluno(request, id):
    aluno = Aluno.objects.get(id=id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'editar_aluno.html', {'form': form, 'aluno': aluno})

@grupo_requerido("Secretaria")
def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_professores')
    else:
        form = ProfessorForm()
    return render(request, 'cadastrar_professor.html', {'form': form})


@grupo_requerido("Secretaria")
def listar_professores(request):
    professores = Professor.objects.all()
    return render(request, 'listar_professor.html', {'professores': professores})