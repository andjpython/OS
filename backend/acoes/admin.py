from django.contrib import admin

from .models import AcaoTecnica, FotoAcao


class FotoAcaoInline(admin.TabularInline):
    model = FotoAcao
    extra = 1


@admin.register(AcaoTecnica)
class AcaoTecnicaAdmin(admin.ModelAdmin):
    list_display = ('ordem_servico', 'profissional', 'data_hora')
    list_filter = ('data_hora',)
    search_fields = ('ordem_servico__numero', 'profissional__nome', 'descricao')
    readonly_fields = ('data_hora',)
    inlines = [FotoAcaoInline]


@admin.register(FotoAcao)
class FotoAcaoAdmin(admin.ModelAdmin):
    list_display = ('acao', 'arquivo', 'criado_em')
    list_filter = ('criado_em',)
    readonly_fields = ('criado_em',)
