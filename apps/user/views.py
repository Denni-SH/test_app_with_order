from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from apps.user.models import User
from apps.user.serializers import UserSerializer


@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

