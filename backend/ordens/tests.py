from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import StatusOS
from pessoas.models import Profissional

from .models import OrdemServico


class OrdemServicoTestCase(TestCase):
    def setUp(self):
        self.status_aberta = StatusOS.objects.create(nome='Aberta', descricao='OS Aberta')
        self.status_finalizada = StatusOS.objects.create(
            nome='Finalizada', descricao='OS Finalizada'
        )
        self.profissional = Profissional.objects.create(nome='João Silva', matricula='1234')

    def test_criar_ordem_servico(self):
        """Testa a criação de uma ordem de serviço"""
        os = OrdemServico.objects.create(
            numero='OS-001', descricao='Teste de OS', status=self.status_aberta
        )
        self.assertEqual(os.numero, 'OS-001')
        self.assertEqual(os.status.nome, 'Aberta')
        self.assertIsNone(os.data_finalizacao)
        self.assertIsNone(os.tempo_total_minutos)

    def test_finalizar_ordem_servico(self):
        """Testa a finalização de OS e cálculo do tempo total"""
        # Criar OS com data de abertura no passado
        data_abertura = timezone.now() - timedelta(hours=2, minutes=30)
        os = OrdemServico.objects.create(
            numero='OS-002',
            descricao='Teste de finalização',
            status=self.status_aberta,
            data_abertura=data_abertura,
        )

        # Finalizar OS
        data_finalizacao = timezone.now()
        os.finalizar(status_final=self.status_finalizada, data_finalizacao=data_finalizacao)

        # Verificar
        os.refresh_from_db()
        self.assertIsNotNone(os.data_finalizacao)
        self.assertEqual(os.status.nome, 'Finalizada')
        # 2h30min = 150 minutos
        self.assertGreaterEqual(os.tempo_total_minutos, 149)
        self.assertLessEqual(os.tempo_total_minutos, 151)

    def test_finalizar_ordem_ja_finalizada(self):
        """Testa que não é possível finalizar uma OS já finalizada"""
        os = OrdemServico.objects.create(
            numero='OS-003', descricao='Teste', status=self.status_aberta
        )

        # Primeira finalização
        os.finalizar(status_final=self.status_finalizada)
        tempo_original = os.tempo_total_minutos

        # Tentar finalizar novamente
        os.finalizar(status_final=self.status_finalizada)

        # Verificar que não mudou
        self.assertEqual(os.tempo_total_minutos, tempo_original)

    def test_associar_profissional_a_os(self):
        """Testa associação de profissional a uma OS"""
        os = OrdemServico.objects.create(
            numero='OS-004', descricao='Teste associação', status=self.status_aberta
        )
        os.profissionais.add(self.profissional)

        self.assertEqual(os.profissionais.count(), 1)
        self.assertEqual(os.profissionais.first().matricula, '1234')

    def test_numero_unico(self):
        """Testa que o número da OS deve ser único"""
        OrdemServico.objects.create(numero='OS-005', status=self.status_aberta)

        with self.assertRaises(Exception):
            OrdemServico.objects.create(numero='OS-005', status=self.status_aberta)
