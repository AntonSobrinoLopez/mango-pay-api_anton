from django.contrib.auth.models import User
from .models import BankAccount, Clients
from mangoApiApp.serializers import UserSerializer, BankAccountSerializer,ClientsSerializer

# Tutorial 6
from rest_framework.decorators import action
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework import permissions
from mangoApiApp.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets

# Refactor con ViewSet - Tutorial 6
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

class ClientsViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    No se muy bien lo que hace
    '''
    queryset= Clients.objects.all()
    serializer_class = ClientsSerializer