from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect


def grupo_requerido(nome_grupo):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=nome_grupo).exists()
    return user_passes_test(in_group)

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
@grupo_requerido("Aluno")
def aluno(request):
    return render(request, 'aluno.html')

@login_required(login_url='/login/')
@grupo_requerido("Professor")
def professor(request):
    return render(request, 'professor.html')

@login_required(login_url='/login/')
@grupo_requerido("Secretaria")
def secretaria(request):
    return render(request, 'secretaria.html')

@login_required(login_url='/login/')
@grupo_requerido("Coordenacao")
def coordenacao(request):
    return render(request, 'coordenaxo.html')

@login_required(login_url='/login/')
@grupo_requerido("Direcao")
def direcao(request):
    return render(request, 'direcao.html')

def erro_403(request, reason=""):
    return render(request, '403.html', status=403)

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
        return redirect('home')
    