from django.db import models
from django.utils import timezone


class Estado(models.Model):
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.sigla


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name="cidades")

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"


class Bairro(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, related_name="bairros")

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    logradouro = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT, related_name="enderecos")

    def __str__(self):
        return f"{self.logradouro}, {self.numero}"


class Pessoa(models.Model):
    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ]

    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    login = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=50)
    gov_validado = models.BooleanField(default=False)
    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="pessoas"
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def autenticar(self, senha):
        return self.senha == senha

    def __str__(self):
        return self.nome


class Paciente(Pessoa):
    pass


class Medico(Pessoa):
    ESPECIALIDADE_CHOICES = [
        ("clinico_geral", "Clínico Geral"),
        ("dermatologia", "Dermatologia"),
        ("ortopedia", "Ortopedia"),
        ("psiquiatria", "Psiquiatria"),
        ("cardiologia", "Cardiologia"),
        ("outra", "Outra"),
    ]

    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.CharField(max_length=50, choices=ESPECIALIDADE_CHOICES)

    def emitir_prescricao(self):
        pass


class Farmacia(models.Model):
    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    login = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=50)
    gov_validado = models.BooleanField(default=False)
    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="farmacias"
    )

    def __str__(self):
        return self.nome


class Farmaceutico(Pessoa):
    crf = models.CharField(max_length=20, unique=True)
    farmacia = models.ForeignKey(
        Farmacia,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="farmaceuticos"
    )

    def validar_prescricao(self):
        pass


class Medicamento(models.Model):
    TARJA_CHOICES = [
        ("sem_tarja", "Sem tarja"),
        ("vermelha", "Tarja vermelha"),
        ("preta", "Tarja preta"),
    ]

    nome = models.CharField(max_length=150)
    principio_ativo = models.CharField(max_length=150, blank=True, null=True)
    dosagem = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=150, blank=True, null=True)
    tarja = models.CharField(max_length=20, choices=TARJA_CHOICES)
    exige_prescricao = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.dosagem}"


class PrescricaoMedica(models.Model):
    STATUS_CHOICES = [
        ("ativa", "Ativa"),
        ("vencida", "Vencida"),
        ("dispensada", "Dispensada"),
        ("cancelada", "Cancelada"),
    ]

    codigo_identificacao = models.CharField(max_length=50, unique=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="prescricoes")
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="prescricoes_emitidas")
    data_emissao = models.DateField(default=timezone.now)
    data_validade = models.DateField()
    orientacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ativa")

    def validar_prescricao(self):
        return self.status == "ativa" and self.data_validade >= timezone.now().date()

    def __str__(self):
        return f"Prescrição {self.codigo_identificacao} - {self.paciente.nome}"


class ItemPrescricao(models.Model):
    prescricao = models.ForeignKey(
        PrescricaoMedica,
        on_delete=models.CASCADE,
        related_name="itens"
    )
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    instrucoes_uso = models.TextField()
    periodo_tratamento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.medicamento.nome} - {self.prescricao.codigo_identificacao}"


class Venda(models.Model):
    farmacia = models.ForeignKey(Farmacia, on_delete=models.PROTECT, related_name="vendas")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="compras")
    prescricao = models.ForeignKey(
        PrescricaoMedica,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="vendas"
    )
    data_hora = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Venda {self.id} - {self.farmacia.nome}"


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.medicamento.nome} - {self.venda.id}"


class UsuarioFake(models.Model):
    PERFIS = [
        ("paciente", "Paciente"),
        ("medico", "Médico"),
        ("farmacia", "Farmácia"),
        ("farmaceutico", "Farmacêutico"),
    ]

    nome = models.CharField(max_length=150)
    documento = models.CharField(max_length=20, unique=True)
    senha = models.CharField(max_length=50)
    perfil = models.CharField(max_length=20, choices=PERFIS)
    gov_validado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.perfil}"