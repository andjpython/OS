from django.contrib import admin

from .models import Colaborador, Profissional


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'matricula')


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'profissao', 'ativo', 'criado_em')
    list_filter = ('ativo', 'profissao')
    search_fields = ('nome', 'email', 'profissao')
