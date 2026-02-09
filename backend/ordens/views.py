from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import StatusOS

from .models import OrdemServico
from .serializers import OrdemServicoFinalizarSerializer, OrdemServicoSerializer


class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all().select_related('status')
    serializer_class = OrdemServicoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_id = self.request.query_params.get('status_id')
        profissional_id = self.request.query_params.get('profissional_id')
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if profissional_id:
            queryset = queryset.filter(profissionais__id=profissional_id)
        return queryset.distinct()

    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        ordem = self.get_object()
        serializer = OrdemServicoFinalizarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_final = serializer.validated_data.get('status')
        if status_final is None:
            status_final, _ = StatusOS.objects.get_or_create(nome='Finalizada')
        ordem.finalizar(status_final=status_final)
        return Response(OrdemServicoSerializer(ordem).data, status=status.HTTP_200_OK)
