from django.urls import path
from deck_app.views import ListarDecks, CriarDecks, EditarDecks, DeletarDecks, Cards

urlpatterns = [
    path('', ListarDecks.as_view(), name='decks'),
    path('novodeck/', CriarDecks.as_view(), name='criar-deck'),
    path('<int:pk>/', EditarDecks.as_view(), name='editar-deck'),
    path('<int:pk>/cards/', Cards.as_view(), name='editar-cards'),
    path('deletar/<int:pk>/', DeletarDecks.as_view(), name='deletar-deck')
]