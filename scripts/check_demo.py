"""Integration checks against the real read-only artifact, without Django's test DB."""
import hashlib
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['HEALTHON_READ_ONLY'] = '1'
os.environ['ALLOWED_HOSTS'] = 'testserver'
os.environ.setdefault('SECRET_KEY', 'integration-check-only-' + 'x' * 60)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthon.settings')
import django
django.setup()
from django.conf import settings
from django.db import connection, OperationalError
from django.test import Client
from django.urls import reverse
from usuarios import urls
from usuarios.models import PrescricaoMedica, UsuarioFake, Medicamento, Venda
from usuarios.demo_seed import MARKER


class ReadOnlyIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.before = hashlib.sha256((ROOT / 'demo/demo.sqlite3').read_bytes()).digest()

    def tearDown(self):
        self.assertEqual(self.before, hashlib.sha256((ROOT / 'demo/demo.sqlite3').read_bytes()).digest())

    def login(self, profile, document):
        response = self.client.post(reverse('login'), {'perfil': profile, 'documento': document, 'senha': 'demo123'}, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.cookies[settings.SESSION_COOKIE_NAME]['secure'])
        return response

    def test_login_dashboards_reads_and_logout_all_profiles(self):
        for profile, document, views in [
            ('medico', '22222222222', ['dashboard_medico', 'paciente_list', 'prescricao_list', 'medicamento_list', 'medico_list']),
            ('paciente', '11111111111', ['dashboard_paciente', 'prescricao_list']),
            ('farmacia', '33333333333', ['dashboard_farmacia', 'farmaceutico_list', 'farmacia_list', 'prescricao_list', 'medicamento_list']),
        ]:
            with self.subTest(profile=profile):
                self.login(profile, document)
                for name in views:
                    response = self.client.get(reverse(name), secure=True)
                    self.assertEqual(response.status_code, 200, name)
                    self.assertIn('no-store', response.headers['Cache-Control'])
                    if name == 'dashboard_paciente':
                        html = response.content.decode()
                        self.assertIn('<div>Medicamento Fictício</div>', html)
                        self.assertIn('<div>10 mg</div>', html)
                own = PrescricaoMedica.objects.get(codigo_identificacao='DEMO-1')
                self.assertEqual(self.client.get(reverse('prescricao_detail', args=[own.pk]), secure=True).status_code, 200)
                self.client.get(reverse('logout'), secure=True)
                self.assertEqual(self.client.get(reverse(views[0]), secure=True).status_code, 302)

    def test_rich_demo_dataset_and_six_original_credentials(self):
        self.assertEqual(UsuarioFake.objects.count(), 6)
        self.assertGreaterEqual(Medicamento.objects.count(), 10)
        seeded = PrescricaoMedica.objects.filter(orientacoes=MARKER)
        self.assertEqual(seeded.count(), 12)
        self.assertEqual(set(seeded.values_list('status', flat=True)), {'ativa', 'vencida', 'dispensada', 'cancelada'})
        self.assertFalse(PrescricaoMedica.objects.filter(itens__isnull=True).exists())
        self.assertEqual(Venda.objects.filter(observacoes=MARKER).count(), 3)
        for profile, document in [('medico', '22222222222'), ('medico', '55555555555'),
                                  ('paciente', '11111111111'), ('paciente', '44444444444'),
                                  ('farmacia', '33333333333'), ('farmacia', '66666666666')]:
            self.login(profile, document)
            for prescription in seeded.select_related('medico', 'paciente'):
                own = profile == 'farmacia' or (profile == 'medico' and prescription.medico.cpf == document) or (profile == 'paciente' and prescription.paciente.cpf == document)
                response = self.client.get(reverse('prescricao_detail', args=[prescription.pk]), secure=True)
                self.assertEqual(response.status_code, 200 if own else 404)
                if own:
                    for item in prescription.itens.select_related('medicamento'):
                        self.assertIn(item.medicamento.nome, response.content.decode())
                        self.assertIn(item.medicamento.dosagem, response.content.decode())
            if profile in {'paciente', 'farmacia'}:
                response = self.client.get(reverse('dashboard_' + profile), secure=True)
                self.assertIn('Cancelada', response.content.decode())
                self.assertIn('Dispensada', response.content.decode())
                self.assertNotIn('Nenhum medicamento informado', response.content.decode())

    def test_all_mutation_urls_blocked_for_every_profile(self):
        for profile, document in [('medico', '22222222222'), ('paciente', '11111111111'), ('farmacia', '33333333333')]:
            self.login(profile, document)
            for route in urls.urlpatterns:
                if route.name.endswith(('_create', '_update', '_delete')) or route.name == 'dispensar_prescricao':
                    args = [1] if '<int:' in str(route.pattern) else []
                    for method in ('get', 'post', 'put', 'patch', 'delete', 'head'):
                        with self.subTest(profile=profile, route=route.name, method=method):
                            self.assertEqual(getattr(self.client, method)(reverse(route.name, args=args), secure=True).status_code, 403)
            self.assertEqual(self.client.post(reverse('prescricao_list'), secure=True).status_code, 403)
        self.assertEqual(self.client.get('/admin/', secure=True).status_code, 404)

    def test_profile_and_record_isolation_in_production(self):
        other = PrescricaoMedica.objects.get(codigo_identificacao='DEMO-2')
        for profile, document, forbidden_dashboard in [
            ('medico', '22222222222', 'dashboard_farmacia'),
            ('paciente', '11111111111', 'dashboard_medico'),
        ]:
            self.login(profile, document)
            self.assertEqual(self.client.get(reverse(forbidden_dashboard), secure=True).status_code, 403)
            self.assertEqual(self.client.get(reverse('prescricao_detail', args=[other.pk]), secure=True).status_code, 404)
            self.assertNotIn(b'DEMO-2', self.client.get(reverse('prescricao_list'), secure=True).content)
        self.login('farmacia', '33333333333')
        page = self.client.get(reverse('farmaceutico_list'), secure=True).content.decode()
        self.assertIn('Farmacêutico Fictício 1', page)
        self.assertNotIn('Farmacêutico Fictício 2', page)
        for path in ['/db.sqlite3', '/demo/demo.sqlite3', '/dados_iniciais.json', '/.env']:
            self.assertEqual(self.client.get(path, secure=True).status_code, 404)

    def test_sqlite_itself_rejects_writes(self):
        with self.assertRaises(OperationalError):
            UsuarioFake.objects.filter(documento='22222222222').update(nome='must fail')
        self.assertIn('mode=ro', str(connection.settings_dict['NAME']))

    def test_invalid_login_csrf_https_and_tampered_cookie(self):
        self.assertEqual(self.client.get('/').status_code, 301)
        self.assertEqual(self.client.post('/', {'perfil': 'medico', 'documento': '22222222222', 'senha': 'wrong'}, secure=True).status_code, 200)
        csrf_client = Client(enforce_csrf_checks=True)
        self.assertEqual(csrf_client.post('/', {'perfil': 'medico'}, secure=True).status_code, 403)
        page = csrf_client.get('/', secure=True)
        token = page.cookies['csrftoken'].value
        self.assertEqual(csrf_client.post('/', {'perfil': 'medico', 'documento': '22222222222', 'senha': 'demo123', 'csrfmiddlewaretoken': token}, secure=True, HTTP_ORIGIN='https://testserver').status_code, 302)
        self.client.cookies[settings.SESSION_COOKIE_NAME] = 'tampered'
        self.assertEqual(self.client.get('/medico/', secure=True).status_code, 302)


if __name__ == '__main__':
    unittest.main(verbosity=2)
