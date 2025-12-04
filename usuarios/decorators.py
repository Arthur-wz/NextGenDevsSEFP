from django.shortcuts import redirect
from django.contrib import messages

print("DECORATOR CARREGADO DE:", __file__)

def grupo_requerido(*nomes_grupos):
    """
    Agora aceita múltiplos grupos:
    @grupo_requerido("Coordenacao", "Direcao")
    @grupo_requerido("Secretaria", "Coordenacao")
    """

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            grupos_user = set(request.user.groups.values_list("name", flat=True))

            # Direção tem acesso total sempre
            if "Direcao" in grupos_user:
                return view_func(request, *args, **kwargs)

            # Qualquer grupo permitido dá acesso
            if grupos_user.intersection(nomes_grupos):
                return view_func(request, *args, **kwargs)

            # Usuário autenticado porém sem permissão
            messages.error(request, "Você não tem permissão para acessar esta página.")

            # Redirecionamento automático para o painel correto
            if "Aluno" in grupos_user:
                return redirect("usuarios:aluno")
            if "Professor" in grupos_user:
                return redirect("usuarios:professor")
            if "Secretaria" in grupos_user:
                return redirect("usuarios:secretaria")
            if "Coordenacao" in grupos_user:
                return redirect("usuarios:coordenacao")
            if "Direcao" in grupos_user:
                return redirect("usuarios:direcao")

            # Caso extremo: usuário sem grupo
            return redirect("login")

        return wrapper

    return decorator
