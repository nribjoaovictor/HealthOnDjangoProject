from datetime import date, timedelta
from decimal import Decimal
from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from .demo_seed import seed_demo, CATALOG, MARKER
from .models import (
    Medico, Paciente, Farmacia, Farmaceutico, UsuarioFake, Medicamento,
    PrescricaoMedica, ItemPrescricao, Venda, ItemVenda,
)


class DemoSeedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.doctors = [Medico.objects.create(nome=f'Médico {i}', cpf=f'm{i}', login=f'm{i}', senha='existing', crm=f'crm{i}', especialidade='clinico_geral') for i in range(2)]
        cls.patients = [Paciente.objects.create(nome=f'Paciente {i}', cpf=f'p{i}', login=f'p{i}', senha='existing', cadastrado_por=cls.doctors[i]) for i in range(2)]
        cls.pharmacies = [Farmacia.objects.create(nome=f'Farmácia {i}', cnpj=f'f{i}', login=f'f{i}', senha='existing') for i in range(2)]
        for i, pharmacy in enumerate(cls.pharmacies):
            Farmaceutico.objects.create(nome=f'Farmacêutico {i}', cpf=f's{i}', login=f's{i}', senha='existing', crf=f'crf{i}', farmacia=pharmacy)
        for profile, entries, field in [('medico', cls.doctors, 'cpf'), ('paciente', cls.patients, 'cpf'), ('farmacia', cls.pharmacies, 'cnpj')]:
            for actor in entries:
                UsuarioFake.objects.create(nome=actor.nome, documento=getattr(actor, field), perfil=profile, senha='existing')

    def test_counts_dates_sales_and_repeat_preserve_original_records(self):
        identities = [Medico, Paciente, Farmacia, Farmaceutico, UsuarioFake]
        before = {model: list(model.objects.order_by('pk').values()) for model in identities}
        legacy = PrescricaoMedica.objects.create(codigo_identificacao='LEGACY', paciente=self.patients[0], medico=self.doctors[0], data_validade=date(2099, 1, 1))
        original = PrescricaoMedica.objects.filter(pk=legacy.pk).values().get()
        first = seed_demo()
        self.assertEqual(first, dict(medicamentos=10, prescricoes=12, itens_prescricao=19, dispensacoes=3, itens_venda=5))
        self.assertEqual(seed_demo(), dict.fromkeys(first, 0))
        for model, records in before.items():
            self.assertEqual(list(model.objects.order_by('pk').values()), records)
        self.assertEqual(PrescricaoMedica.objects.filter(pk=legacy.pk).values().get(), original)
        self.assertEqual(legacy.itens.count(), 1)
        prescriptions = PrescricaoMedica.objects.filter(orientacoes=MARKER)
        self.assertEqual(set(prescriptions.values_list('status', flat=True)), {'ativa', 'vencida', 'dispensada', 'cancelada'})
        for prescription in prescriptions:
            prescription.full_clean()
            self.assertLessEqual(prescription.data_emissao, timezone.localdate())
            self.assertLess(prescription.data_emissao, prescription.data_validade)
            self.assertEqual(prescription.validar_prescricao(), prescription.status == 'ativa')
            self.assertGreater(prescription.itens.count(), 0)
            for item in prescription.itens.select_related('medicamento'):
                item.full_clean()
                self.assertTrue(item.medicamento.dosagem)
            sales = list(prescription.vendas.all())
            self.assertEqual(len(sales), int(prescription.status == 'dispensada'))
            for sale in sales:
                sale.full_clean()
                self.assertEqual(sale.paciente_id, prescription.paciente_id)
                self.assertEqual(sale.data_hora.date(), timezone.localdate() - timedelta(days=1))
                self.assertEqual(sale.valor_total, sum((item.subtotal() for item in sale.itens.all()), Decimal('0')))
                self.assertEqual(set(sale.itens.values_list('medicamento_id', 'quantidade')), set(prescription.itens.values_list('medicamento_id', 'quantidade')))
        self.assertEqual(set(Venda.objects.values_list('farmacia_id', flat=True)), {p.pk for p in self.pharmacies})
        for medicine in Medicamento.objects.all():
            medicine.full_clean()

    def test_reuses_existing_medicine_without_overwriting(self):
        medicine = Medicamento.objects.create(nome='paracetamol', dosagem='500mg', fabricante='Preservar', tarja='sem_tarja')
        before = Medicamento.objects.filter(pk=medicine.pk).values().get()
        self.assertEqual(seed_demo()['medicamentos'], len(CATALOG) - 1)
        self.assertEqual(Medicamento.objects.count(), 10)
        self.assertEqual(Medicamento.objects.filter(pk=medicine.pk).values().get(), before)
        self.assertTrue(ItemPrescricao.objects.filter(medicamento=medicine).exists())

    def test_refuses_missing_identities_without_creating_anything(self):
        Farmacia.objects.all().delete()
        with self.assertRaisesMessage(ValueError, 'Nenhum usuário será criado'):
            seed_demo()
        self.assertEqual(Medicamento.objects.count(), 0)
        self.assertEqual(PrescricaoMedica.objects.count(), 0)

    def test_code_collision_rolls_back_entire_seed(self):
        PrescricaoMedica.objects.create(codigo_identificacao='HO-DEMO-V1-002', paciente=self.patients[0], medico=self.doctors[0], data_validade=date(2099, 1, 1), orientacoes='Original')
        with self.assertRaisesMessage(ValueError, 'Código reservado'):
            seed_demo()
        self.assertEqual(Medicamento.objects.count(), 0)
        self.assertEqual(PrescricaoMedica.objects.count(), 1)
        self.assertEqual(ItemPrescricao.objects.count(), 0)

    def test_rerun_does_not_overwrite_local_edits(self):
        seed_demo()
        prescription = PrescricaoMedica.objects.get(codigo_identificacao='HO-DEMO-V1-001')
        prescription.status = 'cancelada'
        prescription.save()
        seed_demo()
        prescription.refresh_from_db()
        self.assertEqual(prescription.status, 'cancelada')

    def test_seed_command_and_read_only_guard(self):
        output = StringIO()
        call_command('seed_demo', stdout=output)
        self.assertIn('prescricoes=12', output.getvalue())
        with override_settings(READ_ONLY_DEMO=True), self.assertRaises(CommandError):
            call_command('seed_demo')
        self.assertEqual(PrescricaoMedica.objects.count(), 12)

    def test_seed_without_pharmacists_preserves_accounts(self):
        Farmaceutico.objects.all().delete()
        seed_demo()
        self.assertEqual(Farmaceutico.objects.count(), 0)
        self.assertEqual(UsuarioFake.objects.count(), 6)
        self.assertEqual(Venda.objects.count(), 3)

    def test_seeded_views_and_access_for_all_existing_profiles(self):
        seed_demo()
        for profile, entries, field in [('medico', self.doctors, 'cpf'), ('paciente', self.patients, 'cpf'), ('farmacia', self.pharmacies, 'cnpj')]:
            for actor in entries:
                self.client.post(reverse('login'), {'perfil': profile, 'documento': getattr(actor, field), 'senha': 'existing'})
                response = self.client.get(reverse('prescricao_list'))
                self.assertEqual(response.status_code, 200)
                expected = PrescricaoMedica.objects.all()
                if profile == 'medico':
                    expected = expected.filter(medico=actor)
                elif profile == 'paciente':
                    expected = expected.filter(paciente=actor)
                self.assertSetEqual(set(response.context['prescricoes']), set(expected))
                for prescription in PrescricaoMedica.objects.all():
                    detail = self.client.get(reverse('prescricao_detail', args=[prescription.pk]))
                    self.assertEqual(detail.status_code, 200 if prescription in expected else 404)
                    if prescription in expected:
                        for item in prescription.itens.select_related('medicamento'):
                            self.assertContains(detail, item.medicamento.nome)
                            self.assertContains(detail, item.medicamento.dosagem)
                if profile in ('paciente', 'farmacia'):
                    page = self.client.get(reverse('dashboard_' + profile))
                    self.assertContains(page, 'Cancelada')
                    self.assertContains(page, 'Dispensada')
                    self.assertNotContains(page, 'Nenhum medicamento informado')
                    self.assertSetEqual(set(page.context['prescricoes']), set(expected))
                if profile == 'farmacia':
                    staff = self.client.get(reverse('farmaceutico_list'))
                    self.assertTrue(all(s.farmacia_id == actor.pk for s in staff.context['farmaceuticos']))
                    self.assertEqual(self.client.get(reverse('paciente_list')).status_code, 403)
