"""Add fictional clinical examples to existing identities; never change credentials."""
from datetime import timedelta
from decimal import Decimal
import re
from django.db import transaction
from django.utils import timezone
from .models import (
    Medico, Paciente, Farmacia, Medicamento, PrescricaoMedica,
    ItemPrescricao, Venda, ItemVenda,
)

MARKER = 'DEMONSTRAÇÃO ACADÊMICA HEALTHON V1 — dados fictícios, sem finalidade clínica.'
CATALOG = [
    ('Paracetamol', '500 mg, comprimido', 'paracetamol', 'sem_tarja'),
    ('Dipirona', '500 mg/mL, solução oral', 'dipirona monoidratada', 'sem_tarja'),
    ('Ibuprofeno', '200 mg, comprimido', 'ibuprofeno', 'sem_tarja'),
    ('Loratadina', '10 mg, comprimido', 'loratadina', 'sem_tarja'),
    ('Omeprazol', '20 mg, cápsula', 'omeprazol', 'vermelha'),
    ('Amoxicilina', '500 mg, cápsula', 'amoxicilina', 'vermelha'),
    ('Losartana potássica', '50 mg, comprimido', 'losartana potássica', 'vermelha'),
    ('Cloridrato de metformina', '500 mg, comprimido', 'cloridrato de metformina', 'vermelha'),
    ('Sulfato de salbutamol', '100 mcg/dose, aerossol', 'sulfato de salbutamol', 'vermelha'),
    ('Cloreto de sódio', '0,9%, solução nasal', 'cloreto de sódio', 'sem_tarja'),
]


def normalized(value):
    return re.sub(r'\s+', '', value).casefold()


@transaction.atomic
def seed_demo():
    doctors = list(Medico.objects.order_by('pk'))
    patients = list(Paciente.objects.order_by('pk'))
    pharmacies = list(Farmacia.objects.order_by('pk'))
    if not doctors or not patients or not pharmacies:
        raise ValueError('É necessário já existir pelo menos um médico, paciente e farmácia. Nenhum usuário será criado.')
    counts = dict(medicamentos=0, prescricoes=0, itens_prescricao=0, dispensacoes=0, itens_venda=0)
    existing = list(Medicamento.objects.order_by('pk'))
    medicines = []
    for name, dosage, ingredient, label in CATALOG:
        # Compare names and concentrations; reuse legacy records without a presentation.
        medicine = next((m for m in existing if normalized(m.nome) == normalized(name)
                         and (normalized(m.dosagem) == normalized(dosage)
                              or normalized(m.dosagem) == normalized(dosage.split(', ', 1)[0]))), None)
        if medicine is None:
            medicine = Medicamento.objects.create(
                nome=name, dosagem=dosage, principio_ativo=ingredient,
                fabricante='Laboratório Fictício Acadêmico', tarja=label,
                exige_prescricao=label != 'sem_tarja', ativo=True,
            )
            existing.append(medicine)
            counts['medicamentos'] += 1
        medicines.append(medicine)

    today = timezone.localdate()
    for index in range(12):
        # Keep each patient's examples with their existing physician when possible.
        patient = patients[index % len(patients)]
        doctor = doctors[(index // len(patients)) % len(doctors)]
        if patient.cadastrado_por_id:
            doctor = next((d for d in doctors if d.pk == patient.cadastrado_por_id), doctor)
        # Every patient gets varied statuses, even with two or four patients.
        status = ['ativa', 'vencida', 'dispensada', 'cancelada'][(index // len(patients) + index % len(patients)) % 4]
        issued = today - timedelta(days=60 + index if status == 'vencida' else 7 + index)
        valid = issued + timedelta(days=30)
        prescription, created = PrescricaoMedica.objects.get_or_create(
            codigo_identificacao=f'HO-DEMO-V1-{index + 1:03d}',
            defaults=dict(paciente=patient, medico=doctor, data_emissao=issued,
                          data_validade=valid, status=status, orientacoes=MARKER),
        )
        if prescription.orientacoes != MARKER:
            raise ValueError(f'Código reservado já utilizado por outro registro: {prescription.codigo_identificacao}. Nenhuma alteração aplicada.')
        if not created:
            # Do not overwrite edits, add deleted items back or change a dispensed status.
            continue
        counts['prescricoes'] += 1
        for offset in range(1 + index % 2):
            ItemPrescricao.objects.create(
                prescricao=prescription, medicamento=medicines[(index + offset) % len(medicines)],
                quantidade=1 + offset, instrucoes_uso=MARKER,
                periodo_tratamento='7 dias (exemplo fictício)',
            )
            counts['itens_prescricao'] += 1
        if status == 'dispensada':
            pharmacy = pharmacies[(index // len(patients)) % len(pharmacies)]
            sale = Venda.objects.create(farmacia=pharmacy, paciente=patient, prescricao=prescription,
                                        valor_total=Decimal('0.00'), observacoes=MARKER)
            total = Decimal('0.00')
            for item in prescription.itens.all():
                price = Decimal('12.50')
                ItemVenda.objects.create(venda=sale, medicamento=item.medicamento,
                                         quantidade=item.quantidade, preco_unitario=price)
                total += price * item.quantidade
                counts['itens_venda'] += 1
            # Only newly created fictional records are updated.
            Venda.objects.filter(pk=sale.pk).update(valor_total=total, data_hora=timezone.now() - timedelta(days=1))
            counts['dispensacoes'] += 1

    # Add details to existing empty prescriptions without changing any original fields.
    for prescription in PrescricaoMedica.objects.filter(itens__isnull=True).exclude(orientacoes=MARKER).order_by('pk'):
        ItemPrescricao.objects.create(prescricao=prescription, medicamento=medicines[0],
                                     quantidade=1, instrucoes_uso=MARKER,
                                     periodo_tratamento='7 dias (exemplo fictício)')
        counts['itens_prescricao'] += 1
    return counts
