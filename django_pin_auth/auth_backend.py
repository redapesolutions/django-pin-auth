from django.contrib.auth import get_user_model

from .models import SingleUseToken

class PinBackend(object):
    """Authentication backend based on pin value."""
    def authenticate(self, request, email=None, pin=None):
        """Authenticate user based on valid pin."""
        user_model = get_user_model()
        kwargs = {
            user_model.USERNAME_FIELD: email
        }
        try:
            user = user_model.objects.get(**kwargs)
        except user_model.DoesNotExist:
            return None

        # Now that we have the user, check that we have a token
        try:
            token = self._get_token(user, pin)
        except SingleUseToken.DoesNotExist:
            return None

        if token.is_valid():
            # Read token (delete it)
            token.read()
            return user

    def _get_token(self, user, pin):
        """Get the token for corresponding user and pin."""
        return SingleUseToken.objects.get(user=user, token=pin)
