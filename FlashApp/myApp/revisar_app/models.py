from django.db import models
from django.contrib.auth.models import User
from deck_app.models import Deck

# Create your models here.
class Revisao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.DO_NOTHING)
    erros = models.IntegerField()
    acertos = models.IntegerField()
    data_revisao = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f'{self.usuario_id}: {self.deck_id} - erros: {self.erros}, acertos: {self.acertos} (data: {self.data_revisao})'
