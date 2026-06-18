from django.urls import path
from . import views

urlpatterns = [
    path("pacientes/", views.paciente_list, name="paciente_list"),
    path("pacientes/novo/", views.paciente_create, name="paciente_create"),
    path("pacientes/editar/<int:id>/", views.paciente_update, name="paciente_update"),
    path("pacientes/excluir/<int:id>/", views.paciente_delete, name="paciente_delete"),
    path("prescricoes/", views.prescricao_list, name="prescricao_list"),
    path("prescricoes/nova/", views.prescricao_create, name="prescricao_create"),
    path("prescricoes/editar/<int:id>/", views.prescricao_update, name="prescricao_update"),
    path("prescricoes/excluir/<int:id>/", views.prescricao_delete, name="prescricao_delete"),
]