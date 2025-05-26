from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from .models import User,Role, UserRole

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

# UserRoleSerializer para incluir os detalhes do usuário e da role
class UserRoleSerializer(serializers.ModelSerializer):
    # SerializerMethodField para evitar problemas de recursão e customizar a saída
    role_details = RoleSerializer(source='role', read_only=True)

    class Meta:
        model = UserRole
        fields = ('id', 'user', 'role', 'created_at', 'updated_at', 'role_details') 

    def get_role_details(self, obj):
        # Retorna o serializer da role para incluir todos os seus campos
        return RoleSerializer(obj.role).data
    
class UserSerializer(serializers.ModelSerializer):
    roles = UserRoleSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'phone', 'user_hash', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login', 'roles' 
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Modificado para usar .pop() para a senha e user_hash antes de criar o usuário
        password = validated_data.pop('password', None)
        user_hash = validated_data.pop('user_hash', None)

        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        if not user_hash: # Garante que o hash seja gerado se não for fornecido
            import uuid
            user.user_hash = uuid.uuid4().hex
        else:
            user.user_hash = user_hash
        user.save()

        # Atribuir a role padrão "Usuário"
        try:
            default_role = Role.objects.get(name='Usuário') # Buscar pelo nome é mais seguro
            UserRole.objects.create(user=user, role=default_role)
        except Role.DoesNotExist:
            print("AVISO: Role 'Usuário' não encontrada. O usuário foi criado sem uma role padrão.")
        except Exception as e:
            print(f"AVISO: Erro ao atribuir role padrão ao usuário {user.username}: {e}")

        return user
    
    def update(self, instance, validated_data):
        # Lidar com atualização de senha separadamente, se for o caso
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        # Atualizar outros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
 

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.refresh).blacklist()
        except TokenError:
            self.fail('bad_token')