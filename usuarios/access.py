from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from .models import UsuarioFake, Medico, Paciente, Farmacia, PrescricaoMedica
from django.db.models import Q


def profile_required(*profiles, readable=False):
    def decorate(view):
        @wraps(view)
        def checked(request, *args, **kwargs):
            if not request.session.get('usuario_logado'):
                return redirect('login')
            profile = request.session.get('perfil')
            document = request.session.get('documento')
            if profile not in profiles or not UsuarioFake.objects.filter(perfil=profile, documento=document).exists():
                raise PermissionDenied
            model, field = {'medico': (Medico, 'cpf'), 'paciente': (Paciente, 'cpf'), 'farmacia': (Farmacia, 'cnpj')}[profile]
            request.actor = model.objects.filter(**{field: document}).first()
            if request.actor is None:
                raise PermissionDenied
            return view(request, *args, **kwargs)
        checked.demo_readable = readable
        return checked
    return decorate


def prescriptions(request):
    qs = PrescricaoMedica.objects.select_related('paciente', 'medico')
    if request.session['perfil'] == 'medico':
        return qs.filter(medico=request.actor)
    if request.session['perfil'] == 'paciente':
        return qs.filter(paciente=request.actor)
    # Pharmacies consult prescriptions for validation/dispensing, as in the original workflow.
    return qs


def patients(request):
    return Paciente.objects.filter(Q(cadastrado_por=request.actor) | Q(prescricoes__medico=request.actor)).distinct()
