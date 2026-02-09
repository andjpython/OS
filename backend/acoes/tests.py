from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import StatusOS
from ordens.models import OrdemServico
from pessoas.models import Profissional

from .models import AcaoTecnica, FotoAcao


class AcaoTecnicaTestCase(TestCase):
    def setUp(self):
        self.status = StatusOS.objects.create(nome='Em Andamento')
        self.profissional1 = Profissional.objects.create(nome='João', matricula='1111')
        self.profissional2 = Profissional.objects.create(nome='Maria', matricula='2222')
        self.os = OrdemServico.objects.create(numero='OS-100', status=self.status)
        self.os.profissionais.add(self.profissional1)

    def test_criar_acao_tecnica(self):
        """Testa a criação de uma ação técnica"""
        acao = AcaoTecnica.objects.create(
            ordem_servico=self.os,
            profissional=self.profissional1,
            descricao='Instalação de equipamento',
        )
        self.assertEqual(acao.ordem_servico.numero, 'OS-100')
        self.assertEqual(acao.profissional.matricula, '1111')
        self.assertIsNotNone(acao.data_hora)

    def test_profissional_deve_estar_associado_a_os(self):
        """Testa que o profissional deve estar associado à OS"""
        acao = AcaoTecnica(
            ordem_servico=self.os,
            profissional=self.profissional2,  # Não associado à OS
            descricao='Teste',
        )

        with self.assertRaises(ValidationError):
            acao.full_clean()

    def test_profissional_valido_associado_a_os(self):
        """Testa que profissional associado à OS pode criar ação"""
        acao = AcaoTecnica(
            ordem_servico=self.os,
            profissional=self.profissional1,  # Associado à OS
            descricao='Manutenção realizada',
        )
        # Não deve lançar exceção
        acao.full_clean()
        acao.save()
        self.assertIsNotNone(acao.id)


class FotoAcaoTestCase(TestCase):
    def setUp(self):
        self.status = StatusOS.objects.create(nome='Em Andamento')
        self.profissional = Profissional.objects.create(nome='João', matricula='3333')
        self.os = OrdemServico.objects.create(numero='OS-200', status=self.status)
        self.os.profissionais.add(self.profissional)
        self.acao = AcaoTecnica.objects.create(
            ordem_servico=self.os, profissional=self.profissional, descricao='Teste'
        )

    def test_criar_foto_acao(self):
        """Testa a criação de uma foto associada a uma ação"""
        foto = FotoAcao.objects.create(acao=self.acao, arquivo='acoes/foto1.jpg')
        self.assertEqual(foto.acao.id, self.acao.id)
        self.assertIsNotNone(foto.criado_em)

    def test_multiplas_fotos_por_acao(self):
        """Testa que uma ação pode ter múltiplas fotos"""
        FotoAcao.objects.create(acao=self.acao, arquivo='acoes/foto1.jpg')
        FotoAcao.objects.create(acao=self.acao, arquivo='acoes/foto2.jpg')
        FotoAcao.objects.create(acao=self.acao, arquivo='acoes/foto3.jpg')

        self.assertEqual(self.acao.fotos.count(), 3)

    def test_foto_str(self):
        """Testa a representação em string da foto"""
        foto = FotoAcao.objects.create(acao=self.acao, arquivo='acoes/teste.jpg')
        self.assertIn('OS-200', str(foto))
