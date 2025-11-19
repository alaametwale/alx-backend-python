from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class OptionalJWTAuthentication(JWTAuthentication):
    """
    JWTAuthentication subclass that returns None instead of raising when no credentials provided.
    Useful for endpoints that accept both authenticated and unauthenticated access (if needed).
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        return super().authenticate(request)
