# accounts/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import auth, credentials

# Initialize Firebase app once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION')
        if not id_token:
            return None

        if id_token.startswith("Bearer "):
            id_token = id_token[7:]

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')

            user, created = User.objects.get_or_create(username=uid, defaults={"email": email})
            return (user, None)

        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Firebase token invalid: {str(e)}')
