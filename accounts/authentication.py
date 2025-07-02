# accounts/authentication.py
from firebase_admin import auth as firebase_auth, credentials, initialize_app
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

import firebase_admin

if not firebase_admin._apps:
    cred = credentials.Certificate('/etc/secrets/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        id_token = request.headers.get('Authorization')

        if not id_token or not id_token.startswith("Bearer "):
            return None

        id_token = id_token.split("Bearer ")[1]

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email', f'{uid}@firebase.local')

            user, _ = User.objects.get_or_create(username=uid, defaults={"email": email})
            return (user, None)

        except Exception as e:
            print(f"Authentication error: {e}")
            raise AuthenticationFailed("Invalid Firebase ID token.")
