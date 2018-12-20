from django.urls import path

from .views import *

urlpatterns = [
        path('', Index.as_view(), name='index'),
        path('account/', AccountView.as_view(), name='account'),
        path('account/buy-pass/', BuyPassView.as_view(), name='buy_pass'),
        path('login/', Login.as_view(), name='login'),
        path('logout/', Logout.as_view(), name='logout'),
        path('signup/', Signup.as_view(), name='signup'),
]
