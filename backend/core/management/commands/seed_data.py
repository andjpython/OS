"""
Comando para popular o banco de dados com dados de exemplo.
Uso: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from acoes.models import AcaoTecnica
from core.models import StatusOS
from ordens.models import OrdemServico
from pessoas.models import Profissional


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando população do banco...'))

        # Limpar dados existentes (opcional)
        if self.confirm_action('Deseja limpar os dados existentes?'):
            self.limpar_dados()

        # Criar dados
        self.criar_status()
        self.criar_profissionais()
        self.criar_ordens_servico()
        self.criar_acoes_tecnicas()

        self.stdout.write(self.style.SUCCESS('\n✓ Banco de dados populado com sucesso!'))

    def confirm_action(self, message):
        """Solicita confirmação do usuário"""
        resposta = input(f'{message} (s/N): ')
        return resposta.lower() in ['s', 'sim', 'y', 'yes']

    def limpar_dados(self):
        """Limpa os dados existentes"""
        self.stdout.write('  Limpando dados...')
        AcaoTecnica.objects.all().delete()
        OrdemServico.objects.all().delete()
        Profissional.objects.all().delete()
        StatusOS.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  ✓ Dados limpos'))

    def criar_status(self):
        """Cria status de OS"""
        self.stdout.write('\n1. Criando status de OS...')
        status_list = [
            ('Aberta', 'Ordem de serviço aberta'),
            ('Em Andamento', 'Ordem de serviço em execução'),
            ('Aguardando Peças', 'Aguardando chegada de peças'),
            ('Finalizada', 'Ordem de serviço finalizada'),
            ('Cancelada', 'Ordem de serviço cancelada'),
        ]

        for nome, descricao in status_list:
            StatusOS.objects.get_or_create(nome=nome, defaults={'descricao': descricao})
            self.stdout.write(f'  ✓ {nome}')

    def criar_profissionais(self):
        """Cria profissionais"""
        self.stdout.write('\n2. Criando profissionais...')
        profissionais = [
            ('João Silva', '1001'),
            ('Maria Santos', '1002'),
            ('Pedro Oliveira', '1003'),
            ('Ana Costa', '1004'),
            ('Carlos Souza', '1005'),
        ]

        for nome, matricula in profissionais:
            Profissional.objects.get_or_create(
                matricula=matricula, defaults={'nome': nome, 'ativo': True}
            )
            self.stdout.write(f'  ✓ {nome} ({matricula})')

    def criar_ordens_servico(self):
        """Cria ordens de serviço"""
        self.stdout.write('\n3. Criando ordens de serviço...')

        status_aberta = StatusOS.objects.get(nome='Aberta')
        status_andamento = StatusOS.objects.get(nome='Em Andamento')
        status_finalizada = StatusOS.objects.get(nome='Finalizada')

        prof1 = Profissional.objects.get(matricula='1001')
        prof2 = Profissional.objects.get(matricula='1002')
        prof3 = Profissional.objects.get(matricula='1003')

        # OS 1 - Aberta
        os1, created = OrdemServico.objects.get_or_create(
            numero='OS-2026-001',
            defaults={
                'descricao': 'Instalação de equipamento na sala 10',
                'status': status_aberta,
            },
        )
        if created:
            os1.profissionais.add(prof1)
        self.stdout.write(f'  ✓ {os1.numero}')

        # OS 2 - Em andamento
        os2, created = OrdemServico.objects.get_or_create(
            numero='OS-2026-002',
            defaults={
                'descricao': 'Manutenção preventiva - Ar condicionado',
                'status': status_andamento,
            },
        )
        if created:
            os2.profissionais.add(prof1, prof2)
        self.stdout.write(f'  ✓ {os2.numero}')

        # OS 3 - Finalizada
        os3, created = OrdemServico.objects.get_or_create(
            numero='OS-2026-003',
            defaults={
                'descricao': 'Troca de lâmpadas - Corredor principal',
                'status': status_finalizada,
                'data_finalizacao': timezone.now(),
                'tempo_total_minutos': 45,
            },
        )
        if created:
            os3.profissionais.add(prof3)
        self.stdout.write(f'  ✓ {os3.numero}')

        # OS 4 - Em andamento
        os4, created = OrdemServico.objects.get_or_create(
            numero='OS-2026-004',
            defaults={
                'descricao': 'Reparo em sistema elétrico - Sala 25',
                'status': status_andamento,
            },
        )
        if created:
            os4.profissionais.add(prof2, prof3)
        self.stdout.write(f'  ✓ {os4.numero}')

    def criar_acoes_tecnicas(self):
        """Cria ações técnicas"""
        self.stdout.write('\n4. Criando ações técnicas...')

        os1 = OrdemServico.objects.get(numero='OS-2026-001')
        os2 = OrdemServico.objects.get(numero='OS-2026-002')
        prof1 = Profissional.objects.get(matricula='1001')
        prof2 = Profissional.objects.get(matricula='1002')

        acoes = [
            (
                os1,
                prof1,
                'Verificação inicial do local de instalação. '
                'Local adequado, sem necessidade de adaptações.',
            ),
            (
                os2,
                prof1,
                'Início da manutenção preventiva. '
                'Limpeza dos filtros e verificação do sistema.',
            ),
            (
                os2,
                prof2,
                'Teste do sistema após limpeza. '
                'Sistema operando normalmente, temperatura estável.',
            ),
        ]

        for os, prof, descricao in acoes:
            AcaoTecnica.objects.get_or_create(
                ordem_servico=os,
                profissional=prof,
                descricao=descricao,
                defaults={'data_hora': timezone.now()},
            )
            self.stdout.write(f'  ✓ Ação em {os.numero}')
