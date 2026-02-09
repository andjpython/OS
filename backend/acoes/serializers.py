from rest_framework import serializers

from pessoas.models import Profissional

from .models import AcaoTecnica, FotoAcao


class AcaoTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcaoTecnica
        fields = [
            'id',
            'ordem_servico',
            'profissional',
            'descricao',
            'data_hora',
        ]

    def validate(self, attrs):
        ordem = attrs.get('ordem_servico') or getattr(self.instance, 'ordem_servico', None)
        profissional = attrs.get('profissional') or getattr(self.instance, 'profissional', None)
        if ordem and profissional:
            if not ordem.profissionais.filter(id=profissional.id).exists():
                raise serializers.ValidationError(
                    {'profissional': 'Profissional não está associado à OS.'}
                )
        return attrs


class FotoAcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoAcao
        fields = [
            'id',
            'acao',
            'arquivo',
            'criado_em',
        ]
        read_only_fields = ['criado_em']
