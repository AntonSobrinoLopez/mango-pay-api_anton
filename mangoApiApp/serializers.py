from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BankAccount,Clients

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username']

class BankAccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BankAccount
        fields = [
            'user', 'type', 'owner_address', 
            'owner_name', 'tag', 'created_at', 'active'
            ]

class ClientsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Clients
        fields=['name','RegisteredNamestring','ClientId','PrimaryThemeColour',
            'PrimaryButtonColour','Logos','TechEmails','AdminEmails','FraudEmails',
            'Billing_Emails', 'PlatformCategorization','PlatformDescription','PlatformURL',
            'HeadquartersAddress','TaxNumber','CompanyReference']