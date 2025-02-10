from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from apps.user.models import User


class EmailOrPhoneBackend(ModelBackend):
    @staticmethod
    def authenticate(request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
