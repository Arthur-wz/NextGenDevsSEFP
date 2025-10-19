from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps

def grupo_requerido(nome_grupo):
    def decorator(view_func):
        @wraps(view_func)  # Mantém o nome e metadados da view (boa prática)
        @login_required    # Garante que o usuário esteja logado ANTES de checar o grupo
        def _wrapped_view(request, *args, **kwargs):
            # Se o usuário estiver no grupo → permite o acesso
            if request.user.groups.filter(name=nome_grupo).exists():
                return view_func(request, *args, **kwargs)
            # Se estiver logado mas NÃO estiver no grupo → 403 (Proibido)
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
        return _wrapped_view
    return decorator
