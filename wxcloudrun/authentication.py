from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class OpenIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        openid = request.headers.get('Authorization')
        if not openid:
            return None

        try:
            user = User.objects.get(openid=openid)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid openid")

        return (user, None)