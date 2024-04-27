from django.shortcuts import render
from django.views.generic import View
from deck_app.models import Deck


# Create your views here.
class Decks(View):
    def get(self, request):
        print(request)
        contexto = {
            'decks': Deck.objects.all()
        }
        return render(request, 'deck_app/decks.html', context=contexto)