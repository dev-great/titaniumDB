import requests
from jose import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class OktaAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if parts[0].lower() != 'bearer':
            return None
        if len(parts) == 1:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. No credentials provided.')
        elif len(parts) > 2:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain spaces.')

        token = parts[1]
        return self._validate_token(token)

    def _validate_token(self, token):
        try:
            # Decode the token to verify its signature
            decoded_token = jwt.decode(token, settings.OKTA_CLIENT_SECRET,
                                       audience=settings.OKTA_AUDIENCE, issuer=settings.OKTA_ISSUER)
            user_id = decoded_token['sub']
            # Optionally, you can fetch the user from your database
            # user = User.objects.get(id=user_id)
            return (user_id, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.JWTClaimsError:
            raise exceptions.AuthenticationFailed('Invalid claims')
        except Exception as e:
            raise exceptions.AuthenticationFailed(
                'Failed to authenticate token')

        return None
