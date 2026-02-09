from rest_framework import viewsets

from .models import AcaoTecnica, FotoAcao
from .serializers import AcaoTecnicaSerializer, FotoAcaoSerializer


class AcaoTecnicaViewSet(viewsets.ModelViewSet):
    queryset = AcaoTecnica.objects.all().select_related('ordem_servico', 'profissional')
    serializer_class = AcaoTecnicaSerializer


class FotoAcaoViewSet(viewsets.ModelViewSet):
    queryset = FotoAcao.objects.all().select_related('acao')
    serializer_class = FotoAcaoSerializer
