from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

Prescricao = PrescricaoMedica
PrescricaoForm = PrescricaoMedicaForm

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

    prescricoes = Prescricao.objects.select_related("paciente").all().order_by("-data_emissao")

    return render(request, "usuarios/dashboard_farmacia.html", {
        "prescricoes": prescricoes
    })

def dispensar_prescricao(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(Prescricao, id=id)

    if request.method == "POST":
        prescricao.status = "dispensada"
        prescricao.save()

    return redirect("dashboard_farmacia")

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
        prescricao = form.save()
        return redirect("prescricao_detail", id=prescricao.id)

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

def medicamento_list(request):
    if not usuario_logado(request):
        return redirect("login")

    medicamentos = Medicamento.objects.all().order_by("nome")

    return render(request, "usuarios/medicamento_list.html", {
        "medicamentos": medicamentos
    })


def medicamento_create(request):
    if not usuario_logado(request):
        return redirect("login")

    form = MedicamentoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("medicamento_list")

    return render(request, "usuarios/medicamento_form.html", {
        "form": form
    })


def medicamento_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    medicamento = get_object_or_404(Medicamento, id=id)
    form = MedicamentoForm(request.POST or None, instance=medicamento)

    if form.is_valid():
        form.save()
        return redirect("medicamento_list")

    return render(request, "usuarios/medicamento_form.html", {
        "form": form,
        "medicamento": medicamento
    })


def medicamento_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    medicamento = get_object_or_404(Medicamento, id=id)

    if request.method == "POST":
        medicamento.delete()
        return redirect("medicamento_list")

    return render(request, "usuarios/medicamento_confirm_delete.html", {
        "medicamento": medicamento
    })

def prescricao_detail(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(PrescricaoMedica, id=id)
    itens = prescricao.itens.select_related("medicamento").all()

    return render(request, "usuarios/prescricao_detail.html", {
        "prescricao": prescricao,
        "itens": itens,
    })


def item_prescricao_create(request, prescricao_id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(PrescricaoMedica, id=prescricao_id)
    form = ItemPrescricaoForm(request.POST or None)

    if form.is_valid():
        item = form.save(commit=False)
        item.prescricao = prescricao
        item.save()
        return redirect("prescricao_detail", id=prescricao.id)

    return render(request, "usuarios/item_prescricao_form.html", {
        "form": form,
        "prescricao": prescricao,
    })


def item_prescricao_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    item = get_object_or_404(ItemPrescricao, id=id)
    prescricao_id = item.prescricao.id

    if request.method == "POST":
        item.delete()
        return redirect("prescricao_detail", id=prescricao_id)

    return render(request, "usuarios/item_prescricao_confirm_delete.html", {
        "item": item,
    })

def medico_list(request):
    if not usuario_logado(request):
        return redirect("login")

    medicos = Medico.objects.all().order_by("nome")

    return render(request, "usuarios/medico_list.html", {
        "medicos": medicos
    })


def medico_create(request):
    if not usuario_logado(request):
        return redirect("login")

    form = MedicoForm(request.POST or None)

    if form.is_valid():
        medico = form.save()

        UsuarioFake.objects.get_or_create(
            documento=medico.cpf,
            defaults={
                "nome": medico.nome,
                "senha": medico.senha,
                "perfil": "medico",
                "gov_validado": medico.gov_validado,
            }
        )

        return redirect("medico_list")

    return render(request, "usuarios/medico_form.html", {
        "form": form
    })


def medico_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    medico = get_object_or_404(Medico, id=id)
    form = MedicoForm(request.POST or None, instance=medico)

    if form.is_valid():
        form.save()
        return redirect("medico_list")

    return render(request, "usuarios/medico_form.html", {
        "form": form,
        "medico": medico
    })


def medico_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    medico = get_object_or_404(Medico, id=id)

    if request.method == "POST":
        medico.delete()
        return redirect("medico_list")

    return render(request, "usuarios/medico_confirm_delete.html", {
        "medico": medico
    })

def farmacia_list(request):
    if not usuario_logado(request):
        return redirect("login")

    farmacias = Farmacia.objects.all().order_by("nome")

    return render(request, "usuarios/farmacia_list.html", {
        "farmacias": farmacias
    })


def farmacia_create(request):
    if not usuario_logado(request):
        return redirect("login")

    form = FarmaciaForm(request.POST or None)

    if form.is_valid():
        farmacia = form.save()

        UsuarioFake.objects.get_or_create(
            documento=farmacia.cnpj,
            defaults={
                "nome": farmacia.nome,
                "senha": farmacia.senha,
                "perfil": "farmacia",
                "gov_validado": farmacia.gov_validado,
            }
        )

        return redirect("farmacia_list")

    return render(request, "usuarios/farmacia_form.html", {
        "form": form
    })


def farmacia_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmacia = get_object_or_404(Farmacia, id=id)
    form = FarmaciaForm(request.POST or None, instance=farmacia)

    if form.is_valid():
        form.save()
        return redirect("farmacia_list")

    return render(request, "usuarios/farmacia_form.html", {
        "form": form,
        "farmacia": farmacia
    })


def farmacia_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmacia = get_object_or_404(Farmacia, id=id)

    if request.method == "POST":
        farmacia.delete()
        return redirect("farmacia_list")

    return render(request, "usuarios/farmacia_confirm_delete.html", {
        "farmacia": farmacia
    })

def farmaceutico_list(request):
    if not usuario_logado(request):
        return redirect("login")

    farmaceuticos = Farmaceutico.objects.select_related("farmacia").all().order_by("nome")

    return render(request, "usuarios/farmaceutico_list.html", {
        "farmaceuticos": farmaceuticos
    })


def farmaceutico_create(request):
    if not usuario_logado(request):
        return redirect("login")

    form = FarmaceuticoForm(request.POST or None)

    if form.is_valid():
        farmaceutico = form.save()

        UsuarioFake.objects.get_or_create(
            documento=farmaceutico.cpf,
            defaults={
                "nome": farmaceutico.nome,
                "senha": farmaceutico.senha,
                "perfil": "farmaceutico",
                "gov_validado": farmaceutico.gov_validado,
            }
        )

        return redirect("farmaceutico_list")

    return render(request, "usuarios/farmaceutico_form.html", {
        "form": form
    })


def farmaceutico_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmaceutico = get_object_or_404(Farmaceutico, id=id)
    form = FarmaceuticoForm(request.POST or None, instance=farmaceutico)

    if form.is_valid():
        form.save()
        return redirect("farmaceutico_list")

    return render(request, "usuarios/farmaceutico_form.html", {
        "form": form,
        "farmaceutico": farmaceutico
    })


def farmaceutico_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmaceutico = get_object_or_404(Farmaceutico, id=id)

    if request.method == "POST":
        farmaceutico.delete()
        return redirect("farmaceutico_list")

    return render(request, "usuarios/farmaceutico_confirm_delete.html", {
        "farmaceutico": farmaceutico
    })