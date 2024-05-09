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
        contexto = {
            'decks': Deck.objects.all(),
            'mensagem': 'Deck cadastrado com sucesso'
        }
        return render(request, 'deck_app/decks.html', context=contexto)
        