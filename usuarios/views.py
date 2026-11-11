from .access import profile_required, prescriptions, patients
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

Prescricao = PrescricaoMedica
PrescricaoForm = PrescricaoMedicaForm

def usuario_logado(request):
    return request.session.get("usuario_logado")

@profile_required("medico", readable=True)
def dashboard_medico(request):
    if not usuario_logado(request):
        return redirect("login")

    total_pacientes = patients(request).count()
    total_prescricoes = prescriptions(request).count()

    return render(request, "usuarios/dashboard_medico.html", {
        "total_pacientes": total_pacientes,
        "total_prescricoes": total_prescricoes,
    })


@profile_required("paciente", readable=True)
def dashboard_paciente(request):
    if not usuario_logado(request):
        return redirect("login")

    documento = request.session.get("documento")

    paciente = Paciente.objects.filter(cpf=documento).first()

    prescricoes = []

    if paciente:
        prescricoes = (
            Prescricao.objects.filter(paciente=paciente)
            .prefetch_related("itens__medicamento")
            .order_by("-data_emissao")
        )

    return render(request, "usuarios/dashboard_paciente.html", {
        "paciente": paciente,
        "prescricoes": prescricoes
    })


@profile_required("farmacia", readable=True)
def dashboard_farmacia(request):
    if not usuario_logado(request):
        return redirect("login")

    prescricoes = prescriptions(request).prefetch_related("itens__medicamento").order_by("-data_emissao")

    return render(request, "usuarios/dashboard_farmacia.html", {
        "prescricoes": prescricoes
    })

@profile_required("farmacia", readable=False)
def dispensar_prescricao(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(prescriptions(request), id=id)

    if request.method == "POST":
        prescricao.status = "dispensada"
        prescricao.save()

    return redirect("dashboard_farmacia")

@profile_required("medico", readable=True)
def paciente_list(request):
    if not usuario_logado(request):
        return redirect("login")
    pacientes = patients(request).order_by("nome")
    return render(request, "usuarios/paciente_list.html", {"pacientes": pacientes})


@profile_required("medico", readable=False)
def paciente_create(request):
    if not usuario_logado(request):
        return redirect("login")
    form = PacienteForm(request.POST or None)

    if form.is_valid():
        paciente = form.save(commit=False)
        paciente.cadastrado_por = request.actor
        paciente.save()

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


@profile_required("medico", readable=False)
def paciente_update(request, id):
    if not usuario_logado(request):
        return redirect("login")
    paciente = get_object_or_404(patients(request), id=id)
    form = PacienteForm(request.POST or None, instance=paciente)

    if form.is_valid():
        form.save()
        return redirect("paciente_list")

    return render(request, "usuarios/paciente_form.html", {"form": form, "paciente": paciente})


@profile_required("medico", readable=False)
def paciente_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")
    paciente = get_object_or_404(patients(request), id=id)

    if request.method == "POST":
        paciente.delete()
        return redirect("paciente_list")

    return render(request, "usuarios/paciente_confirm_delete.html", {"paciente": paciente})

@profile_required("medico", "paciente", "farmacia", readable=True)
def prescricao_list(request):
    if not usuario_logado(request):
        return redirect("login")

    prescricoes = prescriptions(request)

    return render(
        request,
        "usuarios/prescricao_list.html",
        {"prescricoes": prescricoes}
    )


@profile_required("medico", readable=False)
def prescricao_create(request):
    if not usuario_logado(request):
        return redirect("login")

    form = PrescricaoForm(request.POST or None)
    form.fields["medico"].queryset = Medico.objects.filter(pk=request.actor.pk)
    form.fields["paciente"].queryset = patients(request)

    if form.is_valid():
        form.save()
        return redirect("prescricao_list")

    return render(
        request,
        "usuarios/prescricao_form.html",
        {"form": form}
    )


@profile_required("medico", readable=False)
def prescricao_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(prescriptions(request), id=id)

    form = PrescricaoForm(
        request.POST or None,
        instance=prescricao
    )
    form.fields["medico"].queryset = Medico.objects.filter(pk=request.actor.pk)
    form.fields["paciente"].queryset = patients(request)

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


@profile_required("medico", readable=False)
def prescricao_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(
        prescriptions(request),
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

@profile_required("medico", "farmacia", readable=True)
def medicamento_list(request):
    if not usuario_logado(request):
        return redirect("login")

    medicamentos = Medicamento.objects.all().order_by("nome")

    return render(request, "usuarios/medicamento_list.html", {
        "medicamentos": medicamentos
    })


@profile_required("medico", readable=False)
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


@profile_required("medico", readable=False)
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


@profile_required("medico", readable=False)
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

@profile_required("medico", "paciente", "farmacia", readable=True)
def prescricao_detail(request, id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(prescriptions(request), id=id)
    itens = prescricao.itens.select_related("medicamento").all()

    return render(request, "usuarios/prescricao_detail.html", {
        "prescricao": prescricao,
        "itens": itens,
    })


@profile_required("medico", readable=False)
def item_prescricao_create(request, prescricao_id):
    if not usuario_logado(request):
        return redirect("login")

    prescricao = get_object_or_404(prescriptions(request), id=prescricao_id)
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


@profile_required("medico", readable=False)
def item_prescricao_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    item = get_object_or_404(ItemPrescricao.objects.filter(prescricao__in=prescriptions(request)), id=id)
    prescricao_id = item.prescricao.id

    if request.method == "POST":
        item.delete()
        return redirect("prescricao_detail", id=prescricao_id)

    return render(request, "usuarios/item_prescricao_confirm_delete.html", {
        "item": item,
    })

@profile_required("medico", readable=True)
def medico_list(request):
    if not usuario_logado(request):
        return redirect("login")

    medicos = Medico.objects.filter(pk=request.actor.pk).order_by("nome")

    return render(request, "usuarios/medico_list.html", {
        "medicos": medicos
    })


@profile_required(readable=False)
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


@profile_required("medico", readable=False)
def medico_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    medico = get_object_or_404(Medico.objects.filter(pk=request.actor.pk), id=id)
    form = MedicoForm(request.POST or None, instance=medico)

    if form.is_valid():
        form.save()
        return redirect("medico_list")

    return render(request, "usuarios/medico_form.html", {
        "form": form,
        "medico": medico
    })


@profile_required("medico", readable=False)
def medico_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    medico = get_object_or_404(Medico.objects.filter(pk=request.actor.pk), id=id)

    if request.method == "POST":
        medico.delete()
        return redirect("medico_list")

    return render(request, "usuarios/medico_confirm_delete.html", {
        "medico": medico
    })

@profile_required("farmacia", readable=True)
def farmacia_list(request):
    if not usuario_logado(request):
        return redirect("login")

    farmacias = Farmacia.objects.filter(pk=request.actor.pk).order_by("nome")

    return render(request, "usuarios/farmacia_list.html", {
        "farmacias": farmacias
    })


@profile_required(readable=False)
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


@profile_required("farmacia", readable=False)
def farmacia_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmacia = get_object_or_404(Farmacia.objects.filter(pk=request.actor.pk), id=id)
    form = FarmaciaForm(request.POST or None, instance=farmacia)

    if form.is_valid():
        form.save()
        return redirect("farmacia_list")

    return render(request, "usuarios/farmacia_form.html", {
        "form": form,
        "farmacia": farmacia
    })


@profile_required("farmacia", readable=False)
def farmacia_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmacia = get_object_or_404(Farmacia.objects.filter(pk=request.actor.pk), id=id)

    if request.method == "POST":
        farmacia.delete()
        return redirect("farmacia_list")

    return render(request, "usuarios/farmacia_confirm_delete.html", {
        "farmacia": farmacia
    })

@profile_required("farmacia", readable=True)
def farmaceutico_list(request):
    if not usuario_logado(request):
        return redirect("login")

    farmaceuticos = Farmaceutico.objects.select_related("farmacia").filter(farmacia=request.actor).order_by("nome")

    return render(request, "usuarios/farmaceutico_list.html", {
        "farmaceuticos": farmaceuticos
    })


@profile_required("farmacia", readable=False)
def farmaceutico_create(request):
    if not usuario_logado(request):
        return redirect("login")

    form = FarmaceuticoForm(request.POST or None)
    form.fields["farmacia"].queryset = Farmacia.objects.filter(pk=request.actor.pk)

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


@profile_required("farmacia", readable=False)
def farmaceutico_update(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmaceutico = get_object_or_404(Farmaceutico.objects.filter(farmacia=request.actor), id=id)
    form = FarmaceuticoForm(request.POST or None, instance=farmaceutico)
    form.fields["farmacia"].queryset = Farmacia.objects.filter(pk=request.actor.pk)

    if form.is_valid():
        form.save()
        return redirect("farmaceutico_list")

    return render(request, "usuarios/farmaceutico_form.html", {
        "form": form,
        "farmaceutico": farmaceutico
    })


@profile_required("farmacia", readable=False)
def farmaceutico_delete(request, id):
    if not usuario_logado(request):
        return redirect("login")

    farmaceutico = get_object_or_404(Farmaceutico.objects.filter(farmacia=request.actor), id=id)

    if request.method == "POST":
        farmaceutico.delete()
        return redirect("farmaceutico_list")

    return render(request, "usuarios/farmaceutico_confirm_delete.html", {
        "farmaceutico": farmaceutico
    })
