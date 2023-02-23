from mangoApiApp.views import UserViewSet, BankAccountViewSet,ClientsViewSet
from rest_framework import renderers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mangoApiApp import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename="user")
router.register(r'bank_accounts', views.BankAccountViewSet, basename="bank_account")
router.register(r'Clients',views.ClientsViewSet, basename='clients')

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

# Con Router de REST Framework:
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# Sin Router de REST Framework:
# urlpatterns = format_suffix_patterns([
#     path('', api_root),
#     path('snippets/', snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>/', user_detail, name='user-detail')
# ])