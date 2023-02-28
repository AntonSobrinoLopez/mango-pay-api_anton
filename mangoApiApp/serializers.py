from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BankAccount,Clients,PayInobject,CardWebPayInobject,DirectDebitWebPayInobject,PayPalWebPayInobject

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username']

class BankAccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BankAccount
        # exclude = ('user', 'owner_address')
        fields = [
            'type', 'owner_name', 'tag', 'created_at', 'active'
            ]

class ClientsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Clients
        fields=['name','RegisteredNamestring','ClientId','PrimaryThemeColour',
            'PrimaryButtonColour','Logos','TechEmails','AdminEmails','FraudEmails',
            'Billing_Emails', 'PlatformCategorization','PlatformDescription','PlatformURL',
            'HeadquartersAddress','TaxNumber','CompanyReference']

class PayInobjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PayInobject
        fields=['PaymentTypePayIn','ExecutionType']

class CardWebPayInobjectSerialzer(serializers.HyperlinkedModelSerializer):
    class Meta :
        model = CardWebPayInobject
        fields=['ReturnURL','CardType','SecureMode','Billing','Culture',
                'Shipping','TemplateURL','StatementDescriptor','RedirectURLstring']



class DirectDebitWebPayInobjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= DirectDebitWebPayInobject
        fields=['PaymentTypePayIn','PaymentTypePayIn','SecureMode','Culture','TemplateURL','RedirectURL']


class PayPalWebPayInobjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PayPalWebPayInobject
        fields =['Id','Tag','CreationDate','AuthorId','CreditedUserId','DebitedFunds','CreditedFunds',
                 'Fees','Status','ResultMessage','ExecutionDate','Type','Nature','CreditedWalletId',
                 'DebitedWalletId','PaymentTypePayIn','ExecutionType','RedirectURL',
                 'Culture','ShippingAddress','PaypalBuyerAccountEmail','StatementDescriptor']