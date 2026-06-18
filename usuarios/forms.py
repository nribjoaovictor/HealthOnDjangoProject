from django import forms
from .models import Paciente, Prescricao


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nome",
            "cpf",
            "rg",
            "data_nascimento",
            "sexo",
            "endereco",
            "telefone",
            "email",
            "gov_validado",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control", "placeholder": "000.000.000-00"}),
            "rg": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "sexo": forms.Select(attrs={"class": "form-select"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "gov_validado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        labels = {
            "nome": "Nome completo",
            "cpf": "CPF",
            "rg": "RG",
            "data_nascimento": "Data de nascimento",
            "sexo": "Sexo",
            "endereco": "Endereço",
            "telefone": "Telefone",
            "email": "E-mail",
            "gov_validado": "Validado pelo Gov.br",
        }

class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = [
            "paciente",
            "medicamento",
            "dosagem",
            "orientacoes",
            "data_validade",
            "status",
        ]

        widgets = {
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "medicamento": forms.TextInput(attrs={"class": "form-control"}),
            "dosagem": forms.TextInput(attrs={"class": "form-control"}),
            "orientacoes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "data_validade": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d"
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_validade"].input_formats = ["%Y-%m-%d"]