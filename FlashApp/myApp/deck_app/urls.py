from django.urls import path
from deck_app.views import Decks

urlpatterns = [
    path('', Decks.as_view(), name='decks')
]