from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, Professor, Nota, Advertencia, Turma , Disciplina
from .forms import AlunoForm, ProfessorForm, NotaForm, AdvertenciaForm
from .decorators import grupo_requerido
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Prefetch

# 🔹 Página padrão (não precisa mais ser "Seja bem-vindo", mas deixei por segurança)
def home(request):
    return redirect('login')


# 🔹 Painel do Aluno
@login_required(login_url='/login/')
@grupo_requerido("Aluno")
def aluno(request):
    try:
        aluno = Aluno.objects.get(email=request.user.email)
        notas = Nota.objects.filter(aluno=aluno)
    except Aluno.DoesNotExist:
        aluno = None
        notas = []

    return render(request, 'aluno.html', {
        'aluno': aluno,
        'notas': notas
    })


# 🔹 Painel do Professor
@grupo_requerido("Professor")
def professor(request):
    professor = Professor.objects.filter(user=request.user).first()
    if not professor:
        messages.error(request, "Professor não encontrado.")
        return redirect('login')

    # Turmas e alunos relacionados a esse professor
    turmas = professor.turmas.all()
    alunos = Aluno.objects.filter(turmas__in=turmas).distinct()

    # Notas e advertências desses alunos
    notas = Nota.objects.filter(aluno__in=alunos)
    advertencias = Advertencia.objects.filter(aluno__in=alunos)

    form = NotaForm()

    # Criar nova nota
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nota lançada com sucesso!")
            return redirect('professor')

    context = {
        'professor': professor,
        'turmas': turmas,
        'alunos': alunos,
        'notas': notas,
        'advertencias': advertencias,
        'form': form
    }
    return render(request, 'professor.html', context)

# 🔹 Painel da Secretaria
@grupo_requerido("Secretaria")
def secretaria(request):
    return render(request, 'secretaria.html')



# 🔹 Painel da Coordenação
@grupo_requerido("Coordenacao")
def coordenacao(request):
    if request.method == 'POST':
        form = AdvertenciaForm(request.POST)
        if form.is_valid():
            advertencia = form.save(commit=False)
            advertencia.coordenador = request.user  # força salvar o user logado
            advertencia.save()
            messages.success(request, 'Advertência registrada com sucesso!')
            return redirect('coordenacao')
    else:
        form = AdvertenciaForm()

    advertencias = Advertencia.objects.select_related('aluno', 'coordenador').order_by('-data')

    return render(request, 'coordenacao.html', {
        'form': form,
        'advertencias': advertencias
    })


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
            aluno = form.save(commit=False)

            # → normaliza o nome para gerar username consistente (remove espaços, acentos, etc.)
            base_username = slugify(aluno.nome).replace('-', '_')  # ex: "joao_silva"
            username = base_username

            # → se já existir, **não** cria outro automaticamente: mostra erro e pede alteração
            if User.objects.filter(username=username).exists():
                messages.error(request, f"O login '{username}' já existe. Por favor escolha outro nome ou edite o username antes de salvar.")
                return render(request, 'cadastrar_aluno.html', {'form': form})

            # → cria o usuário com senha padrão
            password = "Al123456#"
            user = User.objects.create_user(username=username, password=password, email=aluno.email or '')
            user.save()

            # → adiciona ao grupo
            grupo_aluno = Group.objects.get(name="Aluno")
            user.groups.add(grupo_aluno)

            # → vincula e salva o aluno
            aluno.user = user
            aluno.save()

            messages.success(request, f"Aluno '{aluno.nome}' cadastrado com sucesso! Login: {username} (senha padrão: {password})")
            return redirect('listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'cadastrar_aluno.html', {'form': form})



@grupo_requerido("Secretaria")
def listar_alunos(request):
    # 1️⃣ Pegamos o termo digitado (caso o usuário tenha feito uma busca)
    termo = request.GET.get('q')

    # 2️⃣ Se o termo tiver conteúdo, filtra os alunos pelo nome (case-insensitive)
    if termo:
        alunos = Aluno.objects.filter(nome__icontains=termo)
    else:
        alunos = Aluno.objects.all()

    # 3️⃣ Retorna o template com a lista e o termo (pra manter o texto no campo)
    return render(request, 'listar_alunos.html', {
        'alunos': alunos,
        'termo': termo
    })

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

def deletar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    aluno.delete()
    return redirect('listar_alunos')

@grupo_requerido("Secretaria")
def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save(commit=False)

            base_username = slugify(professor.nome).replace('-', '_')
            username = base_username

            if User.objects.filter(username=username).exists():
                messages.error(request, f"O login '{username}' já existe. Por favor escolha outro nome ou edite o username antes de salvar.")
                return render(request, 'cadastrar_professor.html', {'form': form})

            password = "Pr123456#"
            user = User.objects.create_user(username=username, password=password, email=professor.email or '')
            user.save()

            grupo_prof = Group.objects.get(name="Professor")
            user.groups.add(grupo_prof)

            professor.user = user
            professor.save()

            messages.success(request, f"Professor '{professor.nome}' cadastrado com sucesso! Login: {username} (senha padrão: {password})")
            return redirect('listar_professores')
    else:
        form = ProfessorForm()
    return render(request, 'cadastrar_professor.html', {'form': form})

@grupo_requerido("Secretaria")
def listar_professores(request):
    # 1️⃣ Pegamos o valor digitado no campo de busca (se existir)
    termo = request.GET.get('q')  # "q" vem do name do input no HTML

    # 2️⃣ Se tiver algo digitado, filtramos pelo nome (usando case-insensitive)
    if termo:
        professores = Professor.objects.filter(nome__icontains=termo)
    else:
        professores = Professor.objects.all()

    # 3️⃣ Renderizamos o template e mandamos o termo junto (pra manter no input)
    return render(request, 'listar_professor.html', {
        'professores': professores,
        'termo': termo
    })

@grupo_requerido("Professor")
def listar_notas_professor(request):
    notas = Nota.objects.filter(professor__user=request.user)
    return render(request, 'listar_notas_professor.html', {'notas': notas})

@grupo_requerido("Professor")
def adicionar_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.professor = Professor.objects.get(user=request.user)
            nota.save()
            return redirect('listar_notas_professor')
    else:
        form = NotaForm()
    return render(request, 'adicionar_nota.html', {'form': form})

def editar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota atualizada com sucesso!')
            return redirect('professor')  # redireciona de volta ao painel
    else:
        form = NotaForm(instance=nota)
    
    return render(request, 'editar_nota.html', {'form': form, 'nota': nota})

def deletar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    nota.delete()
    messages.success(request, 'Nota excluída com sucesso!')
    return redirect('professor')

@grupo_requerido("Secretaria")
def editar_professor(request, id):
    professor = Professor.objects.get(id=id)  # busca o professor pelo ID da URL

    if request.method == 'POST':  # se o formulário foi enviado
        form = ProfessorForm(request.POST, instance=professor)  # cria o form com os novos dados
        if form.is_valid():  # valida o formulário
            form.save()  # salva as alterações no banco
            return redirect('listar_professores')  # redireciona para a listagem
    else:
        form = ProfessorForm(instance=professor)  # carrega o form com os dados antigos

    return render(request, 'editar_professor.html', {'form': form, 'professor': professor})

def deletar_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    professor.delete()
    return redirect('listar_professores')

@grupo_requerido("Coordenacao")
def editar_advertencia(request, id):
    advertencia = get_object_or_404(Advertencia, id=id)
    if request.method == 'POST':
        form = AdvertenciaForm(request.POST, instance=advertencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Advertência atualizada com sucesso!')
            return redirect('coordenacao')
    else:
        form = AdvertenciaForm(instance=advertencia)
    return render(request, 'editar_advertencia.html', {'form': form, 'advertencia': advertencia})


@grupo_requerido("Coordenacao")
def deletar_advertencia(request, id):
    advertencia = get_object_or_404(Advertencia, id=id)
    advertencia.delete()
    messages.success(request, 'Advertência excluída com sucesso!')
    return redirect('coordenacao')

# ===============================
# 🔹 Painel administrativo interno (Coordenação / Direção)
# ===============================

@grupo_requerido("Coordenacao")
def painel_administrativo_coordenacao(request):
    turmas = Turma.objects.prefetch_related(
        Prefetch('alunos', queryset=Aluno.objects.all()),
        Prefetch('disciplinas', queryset=Disciplina.objects.all())
    )
    professores = Professor.objects.all()
    alunos = Aluno.objects.all()
    advertencias = Advertencia.objects.select_related('aluno', 'coordenador').order_by('-data')
    notas = Nota.objects.select_related('aluno', 'disciplina').order_by('-data_lancamento')

    contexto = {
        'turmas': turmas,
        'professores': professores,
        'alunos': alunos,
        'advertencias': advertencias,
        'notas': notas,
    }
    return render(request, 'painel_admin_coordenacao.html', contexto)



@grupo_requerido("Direcao")
def painel_administrativo_direcao(request):
    professores = Professor.objects.all()
    alunos = Aluno.objects.all()
    advertencias = Advertencia.objects.select_related('aluno', 'coordenador')
    notas = Nota.objects.select_related('aluno', 'disciplina')

    contexto = {
        'professores': professores,
        'alunos': alunos,
        'advertencias': advertencias,
        'notas': notas,
    }
    return render(request, 'painel_admin_direcao.html', contexto)
