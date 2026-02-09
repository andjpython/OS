from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class AcaoTecnica(models.Model):
    ordem_servico = models.ForeignKey(
        'os.OrdemServico',
        on_delete=models.CASCADE,
        related_name='acoes',
    )
    profissional = models.ForeignKey(
        'pessoas.Profissional',
        on_delete=models.PROTECT,
        related_name='acoes',
    )
    descricao = models.TextField()
    data_hora = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Ação Técnica'
        verbose_name_plural = 'Ações Técnicas'

    def __str__(self) -> str:
        return f'OS {self.ordem_servico.numero} - {self.profissional.matricula}'

    def clean(self) -> None:
        if not self.ordem_servico_id or not self.profissional_id:
            return
        if not self.ordem_servico.profissionais.filter(id=self.profissional_id).exists():
            raise ValidationError(
                {'profissional': 'Profissional não está associado à OS.'}
            )


class FotoAcao(models.Model):
    acao = models.ForeignKey(
        AcaoTecnica,
        on_delete=models.CASCADE,
        related_name='fotos',
    )
    arquivo = models.FileField(upload_to='acoes/')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto da Ação'
        verbose_name_plural = 'Fotos da Ação'

    def __str__(self) -> str:
        return f'Foto {self.id} - OS {self.acao.ordem_servico.numero}'
