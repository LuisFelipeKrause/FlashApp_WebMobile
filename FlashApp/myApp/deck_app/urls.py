from django.urls import path
from deck_app.views import ListarDecks, CriarDecks

urlpatterns = [
    path('', ListarDecks.as_view(), name='decks'),
    path('novodeck/', CriarDecks.as_view(), name='criar-deck')
]