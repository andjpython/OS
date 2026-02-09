from django.db import models
from django.utils import timezone


class OrdemServico(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True)
    status = models.ForeignKey(
        'core.StatusOS',
        on_delete=models.PROTECT,
        related_name='ordens',
    )
    data_abertura = models.DateTimeField(default=timezone.now)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    tempo_total_minutos = models.PositiveIntegerField(null=True, blank=True)
    profissionais = models.ManyToManyField(
        'pessoas.Profissional',
        through='OrdemServicoProfissional',
        related_name='ordens',
    )

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'

    def __str__(self) -> str:
        return self.numero

    def finalizar(self, status_final: 'core.StatusOS', data_finalizacao=None) -> None:
        if self.data_finalizacao:
            return
        final = data_finalizacao or timezone.now()
        self.data_finalizacao = final
        delta = final - self.data_abertura
        self.tempo_total_minutos = int(delta.total_seconds() // 60)
        self.status = status_final
        self.save(update_fields=['data_finalizacao', 'tempo_total_minutos', 'status'])


class OrdemServicoProfissional(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='ordem_profissionais',
    )
    profissional = models.ForeignKey(
        'pessoas.Profissional',
        on_delete=models.CASCADE,
        related_name='ordem_profissionais',
    )
    data_atribuicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ordem_servico', 'profissional')
        verbose_name = 'Profissional da OS'
        verbose_name_plural = 'Profissionais da OS'

    def __str__(self) -> str:
        return f'{self.ordem_servico.numero} - {self.profissional.matricula}'
