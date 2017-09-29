from django.contrib.auth import get_user_model

from .models import SingleUseToken

class PinBackend(object):
    """Authentication backend based on pin value."""
    def authenticate(self, request, email=None, pin=None):
        """Authenticate user based on valid pin."""
        try:
            token = self._get_token(email, pin)
        except SingleUseToken.DoesNotExist:
            return None

        if token.is_valid():
            # Read token (delete it)
            token.read()
            return token.user

    def _get_token(self, email, pin):
        """Get the token for corresponding user and pin."""
        user_model = get_user_model()
        kwargs = {
            'user__%s' % user_model.USERNAME_FIELD: email,
            'token': pin
        }
        return SingleUseToken.objects.get(**kwargs)

    def get_user(self, user_id):
        """Get user from id."""
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
