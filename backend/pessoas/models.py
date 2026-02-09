from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.db import models


class Profissional(models.Model):
    nome = models.CharField(max_length=120)
    matricula = models.CharField(
        max_length=4,
        unique=True,
        validators=[RegexValidator(r'^\d{4}$', 'A matrícula deve ter 4 dígitos.')],
    )
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'

    def __str__(self) -> str:
        return f'{self.nome} ({self.matricula})'


class Colaborador(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    profissao = models.CharField(max_length=120)
    senha = models.CharField(max_length=128)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'

    def __str__(self) -> str:
        return self.nome

    def set_senha(self, senha: str) -> None:
        self.senha = make_password(senha)
