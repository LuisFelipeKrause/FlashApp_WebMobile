from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Deck(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=300, blank=True, null=True)
    erros = models.IntegerField(default=0)
    acertos = models.IntegerField(default=0)
    num_cards = models.IntegerField(default=0)
    desempenho_geral = models.FloatField(default=0.0)
    criado_em = models.DateTimeField(auto_created=True)
    ultima_revisao = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.titulo}'
    

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    frente = models.CharField(max_length=400)
    verso = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.frente} | {self.verso}'
