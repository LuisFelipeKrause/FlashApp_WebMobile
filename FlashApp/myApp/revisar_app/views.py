from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from deck_app.models import Deck, Card

# Create your views here.
class RevisarCards(LoginRequiredMixin, View):
    def get(self, request, pk):  # Usado para listar o card na revisão
        deck = Deck.objects.filter(id=pk).get()
        cards = Card.objects.filter(deck=pk)

        contexto = {
            'deck': deck,
            'cards': cards
        }
        return render(request, 'revisar_app/revisao.html', contexto)

    # def post()  # Usado para mandar o resultado da revisão
