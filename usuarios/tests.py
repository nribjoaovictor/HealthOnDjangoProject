from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import Medico, Paciente, Farmacia, Farmaceutico, UsuarioFake, PrescricaoMedica


class AccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.doctors = [Medico.objects.create(nome=f'Médico {i}', cpf=f'm{i}', login=f'm{i}', senha='test', crm=f'crm{i}', especialidade='clinico_geral') for i in range(2)]
        cls.patients = [Paciente.objects.create(nome=f'Paciente {i}', cpf=f'p{i}', login=f'p{i}', senha='test', cadastrado_por=cls.doctors[i]) for i in range(2)]
        cls.pharmacies = [Farmacia.objects.create(nome=f'Farmácia {i}', cnpj=f'f{i}', login=f'f{i}', senha='test') for i in range(2)]
        cls.prescriptions = [PrescricaoMedica.objects.create(codigo_identificacao=f'r{i}', medico=cls.doctors[i], paciente=cls.patients[i], data_validade=date(2099, 1, 1)) for i in range(2)]
        cls.staff = [Farmaceutico.objects.create(nome=f'Funcionário {i}', cpf=f's{i}', login=f's{i}', senha='test', crf=f'crf{i}', farmacia=cls.pharmacies[i]) for i in range(2)]
        for profile, entries, field in [('medico', cls.doctors, 'cpf'), ('paciente', cls.patients, 'cpf'), ('farmacia', cls.pharmacies, 'cnpj')]:
            for obj in entries:
                UsuarioFake.objects.create(nome=obj.nome, documento=getattr(obj, field), perfil=profile, senha='test')

    def login_as(self, profile, document):
        response = self.client.post(reverse('login'), {'perfil': profile, 'documento': document, 'senha': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_patient_isolation(self):
        self.login_as('paciente', 'p0')
        self.assertEqual(self.client.get(reverse('dashboard_medico')).status_code, 403)
        self.assertEqual(self.client.get(reverse('paciente_list')).status_code, 403)
        self.assertEqual(self.client.get(reverse('prescricao_detail', args=[self.prescriptions[0].pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('prescricao_detail', args=[self.prescriptions[1].pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse('dispensar_prescricao', args=[self.prescriptions[0].pk])).status_code, 403)
        self.assertQuerySetEqual(self.client.get(reverse('prescricao_list')).context['prescricoes'], [self.prescriptions[0]])

    def test_doctor_isolation(self):
        self.login_as('medico', 'm0')
        self.assertQuerySetEqual(self.client.get(reverse('paciente_list')).context['pacientes'], [self.patients[0]])
        for name in ['prescricao_detail', 'prescricao_update', 'prescricao_delete']:
            self.assertEqual(self.client.get(reverse(name, args=[self.prescriptions[1].pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('paciente_update', args=[self.patients[1].pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('dashboard_farmacia')).status_code, 403)
        self.assertEqual(self.client.get(reverse('medico_create')).status_code, 403)

    def test_pharmacy_isolation(self):
        self.login_as('farmacia', 'f0')
        self.assertQuerySetEqual(self.client.get(reverse('farmaceutico_list')).context['farmaceuticos'], [self.staff[0]])
        self.assertEqual(self.client.get(reverse('farmaceutico_update', args=[self.staff[1].pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('farmacia_update', args=[self.pharmacies[1].pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('paciente_list')).status_code, 403)
        self.assertEqual(self.client.get(reverse('prescricao_update', args=[self.prescriptions[0].pk])).status_code, 403)

    def test_forged_foreign_keys_rejected_locally(self):
        self.login_as('medico', 'm0')
        response = self.client.post(reverse('prescricao_create'), {'codigo_identificacao': 'forged', 'paciente': self.patients[1].pk, 'medico': self.doctors[1].pk, 'data_validade': '2099-01-01', 'status': 'ativa'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PrescricaoMedica.objects.filter(codigo_identificacao='forged').exists())
        self.login_as('farmacia', 'f0')
        response = self.client.get(reverse('farmaceutico_create'))
        self.assertQuerySetEqual(response.context['form'].fields['farmacia'].queryset, [self.pharmacies[0]])

    def test_local_writes_and_signed_cookie_logout(self):
        self.login_as('farmacia', 'f0')
        self.client.post(reverse('dispensar_prescricao', args=[self.prescriptions[0].pk]))
        self.prescriptions[0].refresh_from_db()
        self.assertEqual(self.prescriptions[0].status, 'dispensada')
        self.client.get(reverse('logout'))
        self.assertEqual(self.client.get(reverse('dashboard_farmacia')).status_code, 302)

    def test_new_patient_stays_visible_to_creator(self):
        self.login_as('medico', 'm0')
        response = self.client.post(reverse('paciente_create'), {'nome': 'Novo paciente fictício', 'cpf': 'new', 'login': 'new', 'senha': 'test'})
        self.assertEqual(response.status_code, 302)
        patient = Paciente.objects.get(cpf='new')
        self.assertEqual(patient.cadastrado_por, self.doctors[0])
        self.assertIn(patient, self.client.get(reverse('paciente_list')).context['pacientes'])

    def test_anonymous_and_missing_identity(self):
        self.assertEqual(self.client.get(reverse('prescricao_list')).status_code, 302)
        self.login_as('medico', 'm0')
        UsuarioFake.objects.filter(documento='m0').delete()
        self.assertEqual(self.client.get(reverse('dashboard_medico')).status_code, 403)
