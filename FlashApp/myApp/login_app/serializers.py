from django.contrib.auth.models import User  # Importe o modelo de usuário do Django ou o seu modelo personalizado
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Campo para receber a senha

    class Meta:
        model = User  # Substitua pelo seu modelo de usuário personalizado se aplicável
        fields = ['username', 'password', 'email']  # Campos que serão aceitos para cadastro

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
