def grupos_do_usuario(request):
    if request.user.is_authenticated:
        grupos = request.user.groups.values_list('name', flat=True)
    else:
        grupos = []

    return {
        'is_secretaria': 'Secretaria' in grupos,
        'is_professor': 'Professor' in grupos,
        'is_aluno': 'Aluno' in grupos,
        'is_coordenacao': 'Coordenacao' in grupos,
        'is_direcao': 'Direcao' in grupos,
    }
