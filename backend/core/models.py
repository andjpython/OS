from django.db import models


class StatusOS(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Status da OS'
        verbose_name_plural = 'Status da OS'

    def __str__(self) -> str:
        return self.nome
