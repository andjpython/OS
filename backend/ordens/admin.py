from django.contrib import admin

from .models import OrdemServico, OrdemServicoProfissional


class OrdemServicoProfissionalInline(admin.TabularInline):
    model = OrdemServicoProfissional
    extra = 1


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'status',
        'data_abertura',
        'data_finalizacao',
        'tempo_total_minutos',
    )
    list_filter = ('status', 'data_abertura', 'data_finalizacao')
    search_fields = ('numero', 'descricao')
    readonly_fields = ('data_abertura', 'data_finalizacao', 'tempo_total_minutos')
    inlines = [OrdemServicoProfissionalInline]
