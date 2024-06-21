from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from deck_app.models import Deck, Card
from django.utils import timezone

# Create your views here.
class RevisarCards(LoginRequiredMixin, View):
    def get(self, request, pk):  # Usado para listar o card na revisão
        deck = Deck.objects.filter(id=pk).get()
        cards = Card.objects.filter(deck=pk)

        contexto = {
            'deck': deck,
            'cards': cards,
        }
        return render(request, 'revisar_app/revisao.html', contexto)
    
class ExibirEstatisticas(LoginRequiredMixin, View):
    def get(self, request, pk):
        deck = Deck.objects.filter(id=pk).get()

        total_cards = deck.acertos + deck.erros

        if total_cards < 1:
            total_cards = 1

        acertos_porcentagem = (deck.acertos / total_cards) * 100
        erros_porcentagem = (deck.erros / total_cards) * 100

        contexto = {
            'deck': deck,
            'acertos': acertos_porcentagem,
            'erros': erros_porcentagem,
            'ultima_revisao': deck.ultima_revisao
        }
        return render(request, 'revisar_app/estatisticas.html', contexto)
