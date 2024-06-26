from rest_framework import serializers
from deck_app.models import Deck, Card


class SerializadorDeck(serializers.ModelSerializer):
    """
    Serializador para o model Veículo
    """
    
    class Meta:
        model = Deck
        exclude = []


class SerializadorCard(serializers.ModelSerializer):
    """
    Serializador para o model Veículo
    """
    
    class Meta:
        model = Card
        exclude = []