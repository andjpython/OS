"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from acoes.views import AcaoTecnicaViewSet, FotoAcaoViewSet
from core.views import colaborador_cadastro, public_home
from ordens.views import OrdemServicoViewSet
from pessoas.views import ProfissionalViewSet

router = DefaultRouter()
router.register('ordens', OrdemServicoViewSet, basename='ordens')
router.register('acoes', AcaoTecnicaViewSet, basename='acoes')
router.register('fotos', FotoAcaoViewSet, basename='fotos')
router.register('profissionais', ProfissionalViewSet, basename='profissionais')

admin.site.site_header = 'Sistema de Gestao de Servicos a Industriais'
admin.site.site_title = 'Sistema de Gestao de Servicos a Industriais'
admin.site.index_title = 'Sistema de Gestao de Servicos a Industriais'

urlpatterns = [
    path('', public_home, name='public_home'),
    path('cadastro/', colaborador_cadastro, name='colaborador_cadastro'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
