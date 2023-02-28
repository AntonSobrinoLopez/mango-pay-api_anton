from django.contrib.auth.models import User
from .models import BankAccount, Clients,PayInobject,CardWebPayInobject,DirectDebitWebPayInobject,PayPalWebPayInobject
from mangoApiApp.serializers import UserSerializer, BankAccountSerializer,ClientsSerializer,PayInobjectSerializer,CardWebPayInobjectSerialzer,DirectDebitWebPayInobjectSerializer,PayPalWebPayInobjectSerializer

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
  view Clients for get
    '''
    queryset= Clients.objects.all()
    serializer_class = ClientsSerializer

class PayInobjectViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    View PayInobjectViewSet for get
    '''
    queryset=PayInobject.objects.all()
    serializer_class= PayInobjectSerializer

class CardWebPayInobjectViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    view CardWebPayInobjectViewSet for get
    '''
    queryset= CardWebPayInobject.objects.all()
    serializer_class=CardWebPayInobjectSerialzer

class DirectDebitWebPayInobjectViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    view DirectDebitWebPayInobjectViewSet for get
    '''
    queryset=DirectDebitWebPayInobject.objects.all()
    serializer_class=DirectDebitWebPayInobjectSerializer

class PayPalWebPayInobjectViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    view PayPalWebPayInobjectViewSet for get
    '''
    queryset=PayPalWebPayInobject.objects.all()
    serializer_class=PayPalWebPayInobjectSerializer

class BankAccountPostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]
    


class ClientsPostViewset(viewsets.ModelViewSet):
     """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
     queryset= Clients.objects.all()
     serializer_class = ClientsSerializer
  

class CardWebPayInobjectPostviewsets(viewsets.ModelViewSet):
    queryset=CardWebPayInobject.objects.all()
    serializer_class=CardWebPayInobjectSerialzer

class DirectDebitWebPayInobjectPostviewsets(viewsets.ModelViewSet):
     queryset=DirectDebitWebPayInobject.objects.all()
     serializer_class=DirectDebitWebPayInobjectSerializer

class PayPalWebPayInobjectPostviewsets(viewsets.ModelViewSet):
    queryset=PayPalWebPayInobject.objects.all()
    serializer_class=PayPalWebPayInobjectSerializer