# backends.py
from django.contrib.auth.backends import BaseBackend
from .models import User
from django.utils import timezone

class CustomAuth(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            user.lastAccess = timezone.now()
            user.is_active = True
            user.is_authenticated = True
            user.is_anonymous = False
            user.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
