from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View, ListView, CreateView, UpdateView
from deck_app.models import Deck, Card
from deck_app.forms import FormularioDeck, FormularioCard
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Create your views here.
class ListarDecks(LoginRequiredMixin, ListView):
    model = Deck
    context_object_name = 'decks'
    template_name = 'deck_app/decks.html'


class CriarDecks(LoginRequiredMixin, CreateView):
    model = Deck
    form_class = FormularioDeck
    template_name = 'deck_app/novoDeck.html'
    success_url = reverse_lazy('decks')

    def form_valid(self, form):
        # Define manualmente o usuário para o deck antes de salvar
        form.instance.usuario = self.request.user
        form.instance.criado_em = timezone.now()
        return super().form_valid(form)


class Decks(LoginRequiredMixin, View):
    """def get(self, request):
        contexto = {
            'decks': Deck.objects.filter(usuario_id=request.user.id).all()
        }
        return render(request, 'deck_app/decks.html', context=contexto)"""
    
    """def post(self, request):
        from django.utils import timezone

        titulo = request.POST.get('titulo-deck', None)
        descricao = request.POST.get('descricao', '')

        # Cadastrar o deck
        novo_deck = Deck.objects.filter(usuario=request.user.id, titulo=titulo).first()
        if novo_deck:
            contexto = {
                'decks': Deck.objects.filter(usuario_id=request.user.id).all(),
                'mensagem': 'Você já possui um deck com esse nome'
            }
            return render(request, 'deck_app/decks.html', context=contexto)
        
        novo_deck = Deck.objects.create(titulo=titulo, descricao=descricao, criado_em=timezone.now(), usuario_id=request.user.id)
        try:
            novo_deck.save()
        except:
            contexto = {
                'decks': Deck.objects.filter(usuario_id=request.user.id).all(),
                'mensagem': 'Não foi possível criar o deck',
            }
            return render(request, 'deck_app/decks.html', context=contexto)

        contexto = {
            'decks': Deck.objects.filter(usuario_id=request.user.id).all(),
        }
        return render(request, 'deck_app/decks.html', context=contexto)"""
        

class Cards(View):
    def get(self, request):
        contexto = {
            'cards': Card.objects.all(),
        }
        return render(request, 'deck_app/decks.html', context=contexto)