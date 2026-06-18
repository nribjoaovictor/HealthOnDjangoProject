from django.shortcuts import render, redirect, get_object_or_404
from .models import Paciente, UsuarioFake, Prescricao
from .forms import PacienteForm, PrescricaoForm

def usuario_logado(request):
    return request.session.get("usuario_logado")

def dashboard_medico(request):
    if not usuario_logado(request):
        return redirect("login")

    total_pacientes = Paciente.objects.count()
    total_prescricoes = Prescricao.objects.count()

    return render(request, "usuarios/dashboard_medico.html", {
        "total_pacientes": total_pacientes,
        "total_prescricoes": total_prescricoes,
    })


def dashboard_paciente(request):
    if not usuario_logado(request):
        return redirect("login")

    documento = request.session.get("documento")

    paciente = Paciente.objects.filter(cpf=documento).first()

    prescricoes = []

    if paciente:
        prescricoes = Prescricao.objects.filter(paciente=paciente).order_by("-data_emissao")

    return render(request, "usuarios/dashboard_paciente.html", {
        "paciente": paciente,
        "prescricoes": prescricoes
    })


def dashboard_farmacia(request):
    if not usuario_logado(request):
        return redirect("login")
    return render(request, "usuarios/dashboard_farmacia.html")


def paciente_list(request):
    if not usuario_logado(request):
        return redirect("login")
    pacientes = Paciente.objects.all().order_by("nome")
    return render(request, "usuarios/paciente_list.html", {"pacientes": pacientes})


def paciente_create(request):
    if not usuario_logado(request):
        return redirect("login")
    form = PacienteForm(request.POST or None)

    if form.is_valid():
        paciente = form.save()

        UsuarioFake.objects.get_or_create(
            documento=paciente.cpf,
            defaults={
                "nome": paciente.nome,
                "senha": "123",
                "perfil": "paciente",
                "gov_validado": paciente.gov_validado,
            }
        )

        return redirect("paciente_list")

    return render(request, "usuarios/paciente_form.html", {"form": form})


def paciente_update(request, id):
    if not usuario_logado(request):
        return redirect("login")
    paciente = get_object_or_404(Paciente, id=id)
    form = PacienteForm(request.POST or None, instance=paciente)

    if form.is_valid():
        form.save()
        return redirect("paciente_list")

    return render(request, "usuarios/paciente_form.html", {"form": form, "paciente": paciente})


def paciente_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == "POST":
        paciente.delete()
        return redirect("paciente_list")

    return render(request, "usuarios/paciente_confirm_delete.html", {"paciente": paciente})

def prescricao_list(request):
    if not usuario_logado(request):
        return redirect("login")

    prescricoes = Prescricao.objects.select_related("paciente").all()

    return render(
        request,
        "usuarios/prescricao_list.html",
        {"prescricoes": prescricoes}
    )


def prescricao_create(request):
    if not usuario_logado(request):
        return redirect("login")

    form = PrescricaoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("prescricao_list")

    return render(
        request,
        "usuarios/prescricao_form.html",
        {"form": form}
    )


def prescricao_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(Prescricao, id=id)

    form = PrescricaoForm(
        request.POST or None,
        instance=prescricao
    )

    if form.is_valid():
        form.save()
        return redirect("prescricao_list")

    return render(
        request,
        "usuarios/prescricao_form.html",
        {
            "form": form,
            "prescricao": prescricao
        }
    )


def prescricao_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(
        Prescricao,
        id=id
    )

    if request.method == "POST":
        prescricao.delete()
        return redirect("prescricao_list")

    return render(
        request,
        "usuarios/prescricao_confirm_delete.html",
        {"prescricao": prescricao}
    )