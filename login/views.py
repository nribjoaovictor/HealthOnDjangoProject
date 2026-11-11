from django.shortcuts import render, redirect
from django.contrib import messages
from usuarios.models import UsuarioFake


def login_view(request):
    if request.method == "POST":
        perfil = request.POST.get("perfil")
        documento = request.POST.get("documento")
        senha = request.POST.get("senha")

        usuario = UsuarioFake.objects.filter(
            perfil=perfil,
            documento=documento,
            senha=senha
        ).first()

        if usuario and usuario.perfil in {"medico", "paciente", "farmacia"}:
            request.session.flush()
            request.session["usuario_logado"] = True
            request.session["usuario_nome"] = usuario.nome
            request.session["perfil"] = usuario.perfil
            request.session["documento"] = usuario.documento

            if usuario.perfil == "medico":
                return redirect("dashboard_medico")

            if usuario.perfil == "paciente":
                return redirect("dashboard_paciente")

            if usuario.perfil == "farmacia":
                return redirect("dashboard_farmacia")

        messages.error(request, "Documento, senha ou perfil inválido.")

    return render(request, "login/login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")