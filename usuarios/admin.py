from django.contrib import admin
from .models import (
    UsuarioFake,
    Pessoa,
    Paciente,
    Medico,
    Farmaceutico,
    Farmacia,
    Estado,
    Cidade,
    Bairro,
    Endereco,
    Medicamento,
    PrescricaoMedica,
    ItemPrescricao,
    Venda,
    ItemVenda,
)

admin.site.register(UsuarioFake)
admin.site.register(Pessoa)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Farmaceutico)
admin.site.register(Farmacia)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(Endereco)
admin.site.register(Medicamento)
admin.site.register(PrescricaoMedica)
admin.site.register(ItemPrescricao)
admin.site.register(Venda)
admin.site.register(ItemVenda)