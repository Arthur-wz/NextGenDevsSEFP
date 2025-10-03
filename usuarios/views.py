from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Função auxiliar: checa se o usuário pertence a um grupo
def usuario_do_grupo(user, nome_grupo):
    return user.groups.filter(name=nome_grupo).exists()

# Página inicial (pública)
def home(request):
    return render(request, 'home.html')

# Painéis protegidos por grupo
@login_required(login_url='/login/')
def aluno(request):
    if usuario_do_grupo(request.user, "Aluno"):   # 👈 só se for do grupo "Aluno"
        return render(request, 'aluno.html')
    return HttpResponse("Acesso negado: você não é aluno.")

@login_required(login_url='/login/')
def professor(request):
    if usuario_do_grupo(request.user, "Professor"):
        return render(request, 'professor.html')
    return HttpResponse("Acesso negado: você não é professor.")

@login_required(login_url='/login/')
def secretaria(request):
    if usuario_do_grupo(request.user, "Secretaria"):
        return render(request, 'secretaria.html')
    return HttpResponse("Acesso negado: você não é da secretaria.")

@login_required(login_url='/login/')
def coordenacao(request):
    if usuario_do_grupo(request.user, "Coordenacao"):
        return render(request, 'coordenacao.html')
    return HttpResponse("Acesso negado: você não é da coordenação.")

@login_required(login_url='/login/')
def direcao(request):
    if usuario_do_grupo(request.user, "Direcao"):
        return render(request, 'direcao.html')
    return HttpResponse("Acesso negado: você não é da direção.")
