from django.urls import path
from deck_app.views import ListarDecks, CriarDecks, EditarDecks, DeletarDecks, InfoDeck, Cards

urlpatterns = [
    path('', ListarDecks.as_view(), name='decks'),
    path('novodeck/', CriarDecks.as_view(), name='criar-deck'),
    path('<int:pk>/', EditarDecks.as_view(), name='editar-deck'),
    path('deletar/<int:pk>/', DeletarDecks.as_view(), name='deletar-deck'),
    path('infodeck/<int:pk>/', InfoDeck.as_view(), name='info-deck'),
    path('infodeck/<int:pk>/novocard/', Cards.as_view(), name='criar-card')
]