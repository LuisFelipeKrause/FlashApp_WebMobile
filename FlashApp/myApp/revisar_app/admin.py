from django.contrib import admin
from revisar_app.models import Revisao

# Register your models here.
# Usado para permitir que um usuário administrador possua acesso ao BD, para alterar
class RevisaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'deck','erros', 'acertos', 'data_revisao']
    search_fields = ['titulo', 'usuario']

admin.site.register(Revisao, RevisaoAdmin)