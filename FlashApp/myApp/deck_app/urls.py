from django.urls import path
from deck_app.views import ListarDecks, CriarDecks, EditarDecks, DeletarDecks
from deck_app.views import InfoDeck, CriarCards, EditarCards, DeletarCard, APIListarDecks, APIDeletarDecks, APIAdicionarDeck, APIListarCards

urlpatterns = [
    path('', ListarDecks.as_view(), name='decks'),
    path('api/', APIListarDecks.as_view(), name='api-listar-decks'),
    path('api/novodeck/', APIAdicionarDeck.as_view(), name='api-criar-deck'),
    path('api/revisar/<int:pk>/', APIListarCards.as_view(), name='api-listar-cards'),
    path('novodeck/', CriarDecks.as_view(), name='criar-deck'),
    path('<int:pk>/', EditarDecks.as_view(), name='editar-deck'),
    path('api/<int:pk>/', APIDeletarDecks.as_view(), name='api-deletar-decks'),
    path('deletar/<int:pk>/', DeletarDecks.as_view(), name='deletar-deck'),
    path('infodeck/<int:pk>/', InfoDeck.as_view(), name='info-deck'),
    path('infodeck/<int:pk>/novocard/', CriarCards.as_view(), name='criar-card'),
    path('infodeck/<int:pk>/<int:pk_card>/', EditarCards.as_view(), name='editar-card'),
    path('infodeck/<int:pk>/deletar/<int:pk_card>/', DeletarCard.as_view(), name='deletar-card'),
]