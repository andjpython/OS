from rest_framework import viewsets

from .models import Profissional
from .serializers import ProfissionalSerializer


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        matricula = self.request.query_params.get('matricula')
        if matricula:
            queryset = queryset.filter(matricula=matricula)
        return queryset
