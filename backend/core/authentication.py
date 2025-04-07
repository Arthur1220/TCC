from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CustomCookieJWTAuthentication(JWTAuthentication):
    """
    Tenta obter o token de autenticação primeiro do cookie 'access'.
    Se não existir, utiliza o método padrão (busca no cabeçalho Authorization).
    """
    def get_header(self, request):
        token = request.COOKIES.get('access')
        print("DEBUG - Cookies recebidos:", request.COOKIES)  # Debug
        if token:
            print("DEBUG - Token encontrado no cookie 'access':", token)  # Debug
            return f"Bearer {token}"
        return super().get_header(request)

    def authenticate(self, request):
        header = self.get_header(request)
        print("DEBUG - Cabeçalho de autenticação:", header)  # Debug
        if not header:
            return None

        parts = header.split(" ")
        if len(parts) != 2:
            print("DEBUG - Cabeçalho com formato inválido.")  # Debug
            return None

        token_str = parts[1]
        try:
            validated_token = self.get_validated_token(token_str)
            user = self.get_user(validated_token)
            print("DEBUG - Usuário autenticado:", user)  # Debug
            return (user, validated_token)
        except Exception as e:
            print("DEBUG - Erro ao validar token:", e)  # Debug
            return None
