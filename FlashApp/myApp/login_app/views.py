from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from login_app.serializers import UsuarioSerializer
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework import permissions


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'login_app/home.html')
    

class Cadastro(View):
    def get(self, request):
        return render(request, 'login_app/cadastro.html')
    
    def post(self, request):
        email = request.POST.get('email')

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'login_app/cadastro.html', {'mensagem': 'Digite um e-mail válido'})
        
        username = request.POST.get('nome-usuario')
        senha = request.POST.get('senha')

        usuario = User.objects.filter(email=email).first()
        if usuario:
            return render(request, 'login_app/cadastro.html', {'mensagem': 'Já existe uma conta registrada com esse endereço de e-mail'})
        
        usuario = User.objects.create_user(username=username, email=email, password=senha)
        try:
            usuario.save()
        except:
            return render(request, 'login_app/cadastro.html', {'mensagem': 'Houve algum erro no cadastro'})
    
        Login.post(self, request)
        return redirect('/decks')


class Login(View):
    def get(self, request):
        contexto = {'mensagem': ''}
        if not request.user.is_authenticated:  # Verifica se há uma sessão
            return render(request, 'login_app/login.html', contexto)  # Se não houver sessão, ele renderiza a página de login
        else:
            return redirect('/decks')  # Se houver sessão, ele redireciona para a página inicial da aplicação
    
    def post(self, request):
        # Obtém as credenciais da autenticação do formulário
        email = request.POST.get('email', None)
        senha = request.POST.get('senha', None)

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'login_app/login.html', {'mensagem': 'Digite um e-mail válido'})

        usuario = User.objects.filter(email=email).first()

        if not usuario:
            return render(request, 'login_app/login.html', {'mensagem': 'Usuário ou senha incorretos'})
        
        # Verifica as credenciais de autenticação fornecidas
        user = authenticate(request, username=usuario.username, password=senha)
        if user is not None:
            # Verifica se o usuário ainda está ativo no sistema
            if user.is_active:
                login(request, user)  # Se estiver tudo correto para o login, uma sessão é iniciada
                return redirect('/decks')  # Se o usuário constar no BD e estiver ativo, ele redireciona para a página inicial (isso é o login)
            return render(request, 'login_app/login.html', {'mensagem': 'Usuário inativo'})
        return render(request, 'login_app/login.html', {'mensagem': 'Usuário ou senha incorretos'})
    

class Logout(View):
    def get(self, request):
        logout(request)  # Encerra a sessão
        return redirect(settings.LOGIN_URL)  # Essa constante LOGIN_URL foi definida no arquivo settings.py
    

class APICadastrarUsuario(CreateAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = []
    permission_classes = []

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)

        return user


class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nome': user.username,
            'email': user.email,
            'token': token.key
        })


class LogoutAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Obter o token do usuário autenticado
        token = request.auth
        logout(request)

        # Revogar o token
        token.delete()

        return Response({'mensagem': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
    

class EditAccount(LoginRequiredMixin, View):
    def get(self, request):
        contexto = {
            'nome': request.user,
            'email': request.user.email,
        }
        return render(request, 'login_app/perfil.html', contexto)
    
    def post(self, request):
        user = request.user
        new_name = request.POST.get('name')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')

        if new_name and new_name != user.username:
            user.username = new_name
        
        if new_email and new_email != user.email:
            user.email = new_email
        
        if new_password and new_password != '************':
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

        user.save()
        return redirect('/decks')
        