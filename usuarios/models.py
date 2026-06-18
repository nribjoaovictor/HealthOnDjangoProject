from django.db import models

class Paciente(models.Model):
    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ]

    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gov_validado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class UsuarioFake(models.Model):
    PERFIS = [
        ("paciente", "Paciente"),
        ("medico", "Médico"),
        ("farmacia", "Farmácia"),
    ]

    nome = models.CharField(max_length=150)
    documento = models.CharField(max_length=20, unique=True)
    senha = models.CharField(max_length=50)
    perfil = models.CharField(max_length=20, choices=PERFIS)
    gov_validado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.perfil}"
    
class Prescricao(models.Model):
    STATUS_CHOICES = [
        ("ativa", "Ativa"),
        ("vencida", "Vencida"),
        ("dispensada", "Dispensada"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medicamento = models.CharField(max_length=150)
    dosagem = models.CharField(max_length=100)
    orientacoes = models.TextField()
    data_emissao = models.DateField(auto_now_add=True)
    data_validade = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ativa")

    def __str__(self):
        return f"{self.medicamento} - {self.paciente.nome}"