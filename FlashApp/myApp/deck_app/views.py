from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from deck_app.models import Deck, Card
from deck_app.forms import FormularioDeck, FormularioCard
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


# Create your views here.
# CRUD DE DECKS
class ListarDecks(LoginRequiredMixin, ListView):
    model = Deck
    context_object_name = 'decks'
    template_name = 'deck_app/decks.html'

    def get_queryset(self):
        # Obtém o usuário atualmente logado
        user = self.request.user
        # Filtra os decks pertencentes ao usuário atual
        return Deck.objects.filter(usuario=user)
    

class CriarDecks(LoginRequiredMixin, CreateView):
    model = Deck
    form_class = FormularioDeck
    template_name = 'deck_app/novoDeck.html'
    success_url = reverse_lazy('decks')

    def form_valid(self, form):
        # Define manualmente o usuário para o deck antes de salvar
        form.instance.usuario = self.request.user
        # Define manualmente o horário em que o usuário foi criado
        form.instance.criado_em = timezone.now()
        return super().form_valid(form)
    
    
class EditarDecks(LoginRequiredMixin, UpdateView):
    model = Deck
    form_class = FormularioDeck
    template_name = 'deck_app/editarDeck.html'
    success_url = reverse_lazy('decks')


class DeletarDecks(LoginRequiredMixin, DeleteView):
    model = Deck
    template_name = 'deck_app/deletarDeck.html'
    success_url = reverse_lazy('decks')


# CRUD DE CARDS
class Cards(View):
    def get(self, request, pk):
        deck = get_object_or_404(Deck, pk=pk)
        cards = Card.objects.filter(deck=deck)
        contexto = {
            'deck': deck.titulo,
            'cards': cards
        }
        return render(request, 'deck_app/infoDeck.html', context=contexto)

    #def post(self, request):

