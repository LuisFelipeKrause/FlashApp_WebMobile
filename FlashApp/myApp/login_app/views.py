from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings

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
        usuario = request.POST.get('email', None)
        senha = request.POST.get('senha', None)
        
        # Verifica as credenciais de autenticação fornecidas
        user = authenticate(request, username=usuario, password=senha)
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
    