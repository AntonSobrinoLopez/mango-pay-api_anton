from mangoApiApp.views import UserViewSet, BankAccountViewSet,ClientsViewSet,PayInobjectViewSet,CardWebPayInobjectViewSet,DirectDebitWebPayInobjectViewSet,PayPalWebPayInobjectViewSet,ClientsPostViewset,BankAccountPostViewSet,CardWebPayInobjectPostviewsets,DirectDebitWebPayInobjectPostviewsets,PayPalWebPayInobjectPostviewsets
from rest_framework import renderers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mangoApiApp import views
from django.contrib import admin

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename="user")
router.register(r'bank_accounts', views.BankAccountViewSet, basename="bank_account")
router.register(r'Clients',views.ClientsViewSet, basename='clients')
router.register(r'PayIn',views.PayInobjectViewSet,basename='PayIn')
router.register(r'CardWebPay', views.CardWebPayInobjectViewSet,basename='CardWebPay')
router.register(r'DirectDebitWeb',views.DirectDebitWebPayInobjectViewSet,basename='DirectDebitWeb')
router.register(r'PayPal',views.PayPalWebPayInobjectViewSet,basename='PayPal')

router.register(r'ClientsPost',views.ClientsPostViewset, basename='ClientsPost')
router.register(r'BancAccountPost',views.BankAccountPostViewSet,basename='BankAccountPost')
router.register(r'.CardWebPayInobjectPost',views.CardWebPayInobjectPostviewsets,basename='CardWebPayInobjectPost')
router.register(r'.DirectDebitWebPayInobjectPost',views.DirectDebitWebPayInobjectPostviewsets,basename='DirectDebitWebPayInobjectPost')
router.register(r'.PayPalWebPayInobjectPost',views.PayPalWebPayInobjectPostviewsets,basename='PayPalWebPayInobjectPost')




user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

bank_account_list = BankAccountViewSet.as_view({
    'get': 'list'
})
bank_account_detail = BankAccountViewSet.as_view({
    'get': 'retrieve'
})
clients_list= ClientsViewSet.as_view({
     'get': 'list'
})

clients_detail = ClientsViewSet.as_view({
     'get': 'retrieve'
})


PayInobject_list = PayInobjectViewSet.as_view({
    'get': 'list'
})

PayInobject_Detail = PayInobjectViewSet.as_view({
    'get': 'retrieve'
})

CardWebPayInobject_list = CardWebPayInobjectViewSet.as_view({
    'get': 'list'
})

CardWebPayInobject_Detail = CardWebPayInobjectViewSet.as_view({
    'get': 'retrieve'
})

DirectDebitWebPayInobjectSerializer_list=DirectDebitWebPayInobjectViewSet.as_view({
    'get': 'list'
})

DirectDebitWebPayInobjectSerializer_Detail=DirectDebitWebPayInobjectViewSet.as_view({
    'get': 'retrieve'
})


PayPalWebPayInobjectSerializer_list= PayPalWebPayInobjectViewSet.as_view({
       'get': 'list'
})

PayPalWebPayInobjectSerializer_Detail= PayPalWebPayInobjectViewSet.as_view({
       'get': 'retrieve'
})


######POST#################################################

clients_list_post = ClientsPostViewset.as_view({
    'get': 'list',
    'post': 'create'

})

bank_account_Post_list = BankAccountPostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

CardWebPayInobject_Post_list =CardWebPayInobjectPostviewsets.as_view({
    'get': 'list',
    'post': 'create'
})

DirectDebitWebPayInobject_Post_List=DirectDebitWebPayInobjectPostviewsets.as_view({
    'get': 'list',
    'post': 'create'
})

PayPalWebPayInobject_Post_list=PayPalWebPayInobjectPostviewsets.as_view({
    'get': 'list',
    'post': 'create'
})

# Con Router de REST Framework:
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # path('admin/', admin.site.urls),
]

