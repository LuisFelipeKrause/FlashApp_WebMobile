from django.shortcuts import render
from django.views.generic import View
from deck_app.models import Deck


# Create your views here.
class Decks(View):
    def get(self, request):
        contexto = {
            'decks': Deck.objects.all()
        }
        return render(request, 'deck_app/decks.html', context=contexto)
    
    def post(self, request):
        from django.utils import timezone

        titulo = request.POST.get('titulo-deck', None)
        descricao = request.POST.get('descricao', '')

        # Cadastrar o deck
        novo_deck = Deck.objects.filter(usuario=request.user.id, titulo=titulo).first()
        if novo_deck:
            contexto = {
                'decks': Deck.objects.all(),
                'mensagem': 'Você já possui um deck com esse nome'
            }
            return render(request, 'deck_app/decks.html', context=contexto)
        
        novo_deck = Deck.objects.create(titulo=titulo, descricao=descricao, criado_em=timezone.now(), usuario_id=request.user.id)
        try:
            novo_deck.save()
        except:
            contexto = {
                'decks': Deck.objects.all(),
                'mensagem': 'Não foi possível criar o deck',
            }
            return render(request, 'deck_app/decks.html', context=contexto)

        contexto = {
            'decks': Deck.objects.all(),
        }
        return render(request, 'deck_app/decks.html', context=contexto)
        