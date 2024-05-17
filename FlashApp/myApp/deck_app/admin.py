from django.contrib import admin
from deck_app.models import Deck, Card

# Register your models here.
# Usado para permitir que um usuário administrador possua acesso ao BD, para alterar
class DeckAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'titulo','num_cards', 'erros', 'acertos', 'ultima_revisao']
    search_fields = ['titulo', 'usuario']

admin.site.register(Deck, DeckAdmin)


# Usado para permitir que um usuário administrador possua acesso ao BD, para alterar
class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'deck', 'frente','verso']
    search_fields = ['titulo', 'usuario']

admin.site.register(Card, CardAdmin)