from django.contrib import admin
from .models import UsuarioFake, Paciente, Prescricao

admin.site.register(UsuarioFake)
admin.site.register(Paciente)
admin.site.register(Prescricao)