from django.db import transaction
from rest_framework import serializers

from core.models import StatusOS
from pessoas.models import Profissional

from .models import OrdemServico


class OrdemServicoSerializer(serializers.ModelSerializer):
    profissionais = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Profissional.objects.all(), required=False
    )
    status_nome = serializers.CharField(source='status.nome', read_only=True)

    class Meta:
        model = OrdemServico
        fields = [
            'id',
            'numero',
            'descricao',
            'status',
            'status_nome',
            'data_abertura',
            'data_finalizacao',
            'tempo_total_minutos',
            'profissionais',
        ]
        read_only_fields = ['data_abertura', 'data_finalizacao', 'tempo_total_minutos']

    @transaction.atomic
    def create(self, validated_data):
        profissionais = validated_data.pop('profissionais', [])
        ordem = super().create(validated_data)
        if profissionais:
            ordem.profissionais.set(profissionais)
        return ordem

    @transaction.atomic
    def update(self, instance, validated_data):
        profissionais = validated_data.pop('profissionais', None)
        ordem = super().update(instance, validated_data)
        if profissionais is not None:
            ordem.profissionais.set(profissionais)
        return ordem


class OrdemServicoFinalizarSerializer(serializers.Serializer):
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=StatusOS.objects.all(),
        required=False,
        allow_null=True,
        source='status',
    )
