from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from deck_app.models import Deck
from rest_framework.authtoken.models import Token
from datetime import datetime

class DeckListTests(APITestCase):
    @classmethod
    def setUpTestData(self):
        # Cria um usuário para associar aos decks
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Cria um token para o usuário
        self.token = Token.objects.create(user=self.user)

        # Cria alguns objetos Deck
        Deck.objects.create(
            usuario=self.user, 
            titulo="Deck 1", 
            descricao="Descrição 1", 
            erros=0, 
            acertos=0, 
            num_cards=5, 
            desempenho_geral=0, 
            criado_em=datetime.now(),
            ultima_revisao=None
        )
        Deck.objects.create(
            usuario=self.user, 
            titulo="Deck 2", 
            descricao="Descrição 2", 
            erros=0, 
            acertos=0, 
            num_cards=5, 
            desempenho_geral=0, 
            criado_em=datetime.now(),
            ultima_revisao=None
        )
        Deck.objects.create(
            usuario=self.user, 
            titulo="Deck 3", 
            descricao="Descrição 3", 
            erros=0, 
            acertos=0, 
            num_cards=5, 
            desempenho_geral=0, 
            criado_em=datetime.now(),
            ultima_revisao=None
        )

    def test_list_decks(self):
        """
        Testa a listagem de objetos Deck com autenticação por token
        """
        # Autentica o cliente com o token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.url = reverse('decks')  # Substitua pelo nome correto da sua rota de listagem
        response = self.client.get(self.url)
        
        # Verifica se a resposta está OK (status 200)
        self.assertEqual(response.status_code, 302)
        
        # Verifica se o número de objetos na resposta é o esperado
        self.assertEqual(len(response.context.get('decks')), 3)
        
        # Verifica se os títulos dos objetos estão corretos
        expected_titles = ["Deck 1", "Deck 2", "Deck 3"]
        returned_titles = [deck['titulo'] for deck in response.context.get('decks')]
        self.assertListEqual(returned_titles, expected_titles)

