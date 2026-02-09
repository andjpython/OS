from django.contrib import admin

from .models import StatusOS


@admin.register(StatusOS)
class StatusOSAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)
