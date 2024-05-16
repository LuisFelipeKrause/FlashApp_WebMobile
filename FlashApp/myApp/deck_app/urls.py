from django.urls import path
from deck_app.views import ListarDecks, CriarDecks, EditarDeck

urlpatterns = [
    path('', ListarDecks.as_view(), name='decks'),
    path('novodeck/', CriarDecks.as_view(), name='criar-deck'),
    path('<int:pk>/', EditarDeck.as_view(), name='editar-deck'),
]