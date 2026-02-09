from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from .models import Profissional


class ProfissionalTestCase(TestCase):
    def test_criar_profissional(self):
        """Testa a criação de um profissional"""
        prof = Profissional.objects.create(nome='Maria Santos', matricula='5678')
        self.assertEqual(prof.nome, 'Maria Santos')
        self.assertEqual(prof.matricula, '5678')
        self.assertTrue(prof.ativo)

    def test_matricula_deve_ter_4_digitos(self):
        """Testa validação da matrícula (4 dígitos)"""
        prof = Profissional(nome='João', matricula='123')  # 3 dígitos - inválido
        with self.assertRaises(ValidationError):
            prof.full_clean()

        prof2 = Profissional(nome='João', matricula='12345')  # 5 dígitos - inválido
        with self.assertRaises(ValidationError):
            prof2.full_clean()

        prof3 = Profissional(nome='João', matricula='abcd')  # letras - inválido
        with self.assertRaises(ValidationError):
            prof3.full_clean()

    def test_matricula_unica(self):
        """Testa que a matrícula deve ser única"""
        Profissional.objects.create(nome='Profissional 1', matricula='1111')

        with self.assertRaises(IntegrityError):
            Profissional.objects.create(nome='Profissional 2', matricula='1111')

    def test_profissional_str(self):
        """Testa a representação em string do profissional"""
        prof = Profissional.objects.create(nome='Pedro Oliveira', matricula='9999')
        self.assertEqual(str(prof), 'Pedro Oliveira (9999)')
