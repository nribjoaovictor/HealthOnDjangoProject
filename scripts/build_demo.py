"""Create a fresh fictional database. Never opens or copies db.sqlite3."""
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthon.settings')


def build():
    import django
    from django.conf import settings
    from django.core.management import call_command
    from django.db import connections

    target = ROOT / 'demo' / 'demo.sqlite3'
    target.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as directory:
        temporary = Path(directory) / 'fictional.sqlite3'
        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3', 'NAME': temporary,
        }
        django.setup()
        call_command('migrate', interactive=False, verbosity=0)
        from usuarios.models import Paciente, Medico, Farmacia, Farmaceutico, UsuarioFake, Medicamento, PrescricaoMedica, ItemPrescricao
        from datetime import date

        doctor = Medico.objects.create(nome='Médica Demonstração A', cpf='22222222222', login='demo-medico-a', senha='demo123', crm='DEMO-A', especialidade='clinico_geral')
        other_doctor = Medico.objects.create(nome='Médico Demonstração B', cpf='55555555555', login='demo-medico-b', senha='demo123', crm='DEMO-B', especialidade='clinico_geral')
        pharmacy = Farmacia.objects.create(nome='Farmácia Fictícia A', cnpj='33333333333', login='demo-farmacia-a', senha='demo123')
        other_pharmacy = Farmacia.objects.create(nome='Farmácia Fictícia B', cnpj='66666666666', login='demo-farmacia-b', senha='demo123')
        medicine = Medicamento.objects.create(nome='Medicamento Fictício', dosagem='10 mg', tarja='sem_tarja')
        for i, (document, physician) in enumerate([('11111111111', doctor), ('44444444444', other_doctor)], 1):
            patient = Paciente.objects.create(nome=f'Paciente Fictício {i}', cpf=document, login=f'demo-paciente-{i}', senha='demo123', cadastrado_por=physician)
            prescription = PrescricaoMedica.objects.create(codigo_identificacao=f'DEMO-{i}', paciente=patient, medico=physician, data_emissao=date(2026, 1, 1), data_validade=date(2099, 12, 31), orientacoes='Exemplo fictício, sem finalidade clínica.')
            ItemPrescricao.objects.create(prescricao=prescription, medicamento=medicine, instrucoes_uso='Exemplo de demonstração.')
            UsuarioFake.objects.create(nome=patient.nome, documento=document, perfil='paciente', senha='demo123')
        for i, unit in enumerate([pharmacy, other_pharmacy], 1):
            Farmaceutico.objects.create(nome=f'Farmacêutico Fictício {i}', cpf=f'7777777777{i}', login=f'demo-funcionario-{i}', senha='demo123', crf=f'DEMO-{i}', farmacia=unit)
        for profile, entries, field in [('medico', [doctor, other_doctor], 'cpf'), ('farmacia', [pharmacy, other_pharmacy], 'cnpj')]:
            for entry in entries:
                UsuarioFake.objects.create(nome=entry.nome, documento=getattr(entry, field), perfil=profile, senha='demo123')
        from usuarios.demo_seed import seed_demo
        counts = seed_demo()
        print('Seed acadêmico:', counts)
        connections.close_all()
        os.replace(temporary, target)
    print('Banco fictício gerado em demo/demo.sqlite3; banco local preservado.')


if __name__ == '__main__':
    build()
