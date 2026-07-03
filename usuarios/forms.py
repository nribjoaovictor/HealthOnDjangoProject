from django import forms
from .models import (
    Paciente,
    Medico,
    Farmaceutico,
    Farmacia,
    Medicamento,
    PrescricaoMedica,
    ItemPrescricao,
    Venda,
)


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nome", "cpf", "rg", "data_nascimento", "sexo",
            "telefone", "email", "login", "senha", "gov_validado"
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "rg": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "sexo": forms.Select(attrs={"class": "form-select"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "login": forms.TextInput(attrs={"class": "form-control"}),
            "senha": forms.PasswordInput(attrs={"class": "form-control"}),
            "gov_validado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            "nome", "cpf", "rg", "data_nascimento", "sexo",
            "telefone", "email", "login", "senha", "gov_validado",
            "crm", "especialidade"
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "rg": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "sexo": forms.Select(attrs={"class": "form-select"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "login": forms.TextInput(attrs={"class": "form-control"}),
            "senha": forms.PasswordInput(attrs={"class": "form-control"}),
            "gov_validado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "crm": forms.TextInput(attrs={"class": "form-control"}),
            "especialidade": forms.Select(attrs={"class": "form-select"}),
        }


class FarmaceuticoForm(forms.ModelForm):
    class Meta:
        model = Farmaceutico
        fields = [
            "nome", "cpf", "rg", "data_nascimento", "sexo",
            "telefone", "email", "login", "senha", "gov_validado",
            "crf", "farmacia"
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "rg": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "sexo": forms.Select(attrs={"class": "form-select"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "login": forms.TextInput(attrs={"class": "form-control"}),
            "senha": forms.PasswordInput(attrs={"class": "form-control"}),
            "gov_validado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "crf": forms.TextInput(attrs={"class": "form-control"}),
            "farmacia": forms.Select(attrs={"class": "form-select"}),
        }


class FarmaciaForm(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = [
            "nome",
            "cnpj",
            "telefone",
            "email",
            "login",
            "senha",
            "gov_validado",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "login": forms.TextInput(attrs={"class": "form-control"}),
            "senha": forms.PasswordInput(attrs={"class": "form-control"}),
            "gov_validado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            "nome", "principio_ativo", "dosagem",
            "fabricante", "tarja", "exige_prescricao", "ativo"
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "principio_ativo": forms.TextInput(attrs={"class": "form-control"}),
            "dosagem": forms.TextInput(attrs={"class": "form-control"}),
            "fabricante": forms.TextInput(attrs={"class": "form-control"}),
            "tarja": forms.Select(attrs={"class": "form-select"}),
            "exige_prescricao": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class PrescricaoMedicaForm(forms.ModelForm):
    class Meta:
        model = PrescricaoMedica
        fields = [
            "codigo_identificacao",
            "paciente",
            "medico",
            "data_validade",
            "orientacoes",
            "status",
        ]
        widgets = {
            "data_validade": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class ItemPrescricaoForm(forms.ModelForm):
    class Meta:
        model = ItemPrescricao
        fields = [
            "medicamento",
            "quantidade",
            "instrucoes_uso",
            "periodo_tratamento",
        ]

        widgets = {
            "medicamento": forms.Select(attrs={"class": "form-select"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control"}),
            "instrucoes_uso": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "periodo_tratamento": forms.TextInput(attrs={"class": "form-control"}),
        }


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
            "farmacia",
            "paciente",
            "prescricao",
            "valor_total",
            "observacoes",
        ]