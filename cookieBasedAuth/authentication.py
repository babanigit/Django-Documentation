from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Try to get the token from cookies
        token = request.COOKIES.get(settings.AUTH_COOKIE)

        if token:
            try:
                validated_token = self.get_validated_token(token)
                return self.get_user(validated_token), validated_token
            except AuthenticationFailed:
                pass  # If cookie token fails, try Authorization header

        # Try the Authorization header if cookie-based auth fails
        return super().authenticate(request)
