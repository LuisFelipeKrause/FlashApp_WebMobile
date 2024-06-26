from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from deck_app.models import Deck, Card
from deck_app.forms import FormularioDeck, FormularioCard
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from deck_app.serializers import SerializadorDeck
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from revisar_app.models import Revisao
from deck_app.serializers import SerializadorCard


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


class InfoDeck(LoginRequiredMixin, View):
    def get(self, request, pk):
        deck = get_object_or_404(Deck, pk=pk)
        cards = Card.objects.filter(deck=deck)
        contexto = {
            'deck': deck,
            'cards': cards
        }
        return render(request, 'deck_app/infoDeck.html', context=contexto)
    
    def post(self, request, pk):
        erros = request.POST.get('erros-form')
        acertos = request.POST.get('acertos-form')
        data_revisao = timezone.now()

        deck = get_object_or_404(Deck, pk=pk)

        deck.erros += int(erros)
        deck.acertos += int(acertos)
        deck.ultima_revisao = data_revisao
        deck.save()

        revisao = Revisao(usuario=request.user, deck=deck, erros=erros, acertos=acertos, data_revisao=data_revisao)
        revisao.save()

        return self.get(request, pk)


# CRUD DE CARDS
class CriarCards(LoginRequiredMixin, CreateView):
    model = Card
    form_class = FormularioCard
    template_name = 'deck_app/novoCard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['pk'] = pk
        # Adicione outros contextos aqui, se necessário
        return context
    
    def form_valid(self, form):
        deck_pk = self.kwargs.get('pk')
        deck = Deck.objects.filter(id=deck_pk).get()
        form.instance.deck = deck
        deck.num_cards += 1
        deck.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        # Obtendo o pk do deck a partir dos parâmetros da URL
        deck_pk = self.kwargs.get('pk')
        return reverse('info-deck', kwargs={'pk': deck_pk})
    

class EditarCards(LoginRequiredMixin, UpdateView):
    model = Card
    form_class = FormularioCard
    template_name = 'deck_app/editarCard.html'

    def get_object(self, queryset=None):
        pk_card = self.kwargs.get('pk_card')
        return Card.objects.get(pk=pk_card)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['pk'] = pk
        pk_card = self.kwargs.get('pk_card')
        context['pk_card'] = pk_card
        # Adicione outros contextos aqui, se necessário
        return context
    
    def form_valid(self, form):
        deck_pk = self.kwargs.get('pk')
        deck = Deck.objects.filter(id=deck_pk).get()
        form.instance.deck = deck
        return super().form_valid(form)

    def get_success_url(self):
        # Obtendo o pk do deck a partir dos parâmetros da URL
        deck_pk = self.kwargs.get('pk')
        return reverse('info-deck', kwargs={'pk': deck_pk})


class DeletarCard(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'deck_app/deletarCard.html'
    
    def get_object(self, queryset=None):
        pk_card = self.kwargs.get('pk_card')
        return Card.objects.get(pk=pk_card)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['pk'] = pk
        # Adicione outros contextos aqui, se necessário
        return context
    
    def form_valid(self, form):
        deck_pk = self.kwargs.get('pk')
        deck = Deck.objects.filter(id=deck_pk).get()
        deck.num_cards -= 1
        deck.save()
        return super().form_valid(form)

    def get_success_url(self):
        deck_pk = self.kwargs.get('pk')
        return reverse('info-deck', kwargs={'pk': deck_pk})


# CRUD API
class APIListarDecks(ListAPIView):
    serializer_class = SerializadorDeck
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Deck.objects.filter(usuario=user)
    

class APIDeletarDecks(DestroyAPIView):
    serializer_class = SerializadorDeck
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Deck.objects.filter(usuario=user)
    
    def perform_destroy(self, instancia):
        # Antes de excluir o deck, exclua todos os cards associados a ele
        cards = Card.objects.filter(deck=instancia)
        cards.delete()
        # Agora pode excluir o próprio deck
        instancia.delete()
    

class APIAdicionarDeck(CreateAPIView):
    serializer_class = SerializadorDeck
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class APIAdicionarCard(CreateAPIView):
    serializer_class = SerializadorCard
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        deck = Deck.objects.filter(id=self.kwargs['pk']).get()
        serializer.save(deck=deck)


class APIListarCards(ListAPIView):
    serializer_class = SerializadorCard
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        deck = self.kwargs['pk']
        return Card.objects.filter(deck=deck)