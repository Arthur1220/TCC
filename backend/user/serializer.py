from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'cpf', 'password', 'created_at']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            cpf=validated_data['cpf']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail('bad_token')