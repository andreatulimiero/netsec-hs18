from django.urls import path

from .views import *

urlpatterns = [
        path('', Index.as_view(), name='index'),
        path('passes/', PassCRUD.as_view(), name='passes'),
        path('passes/<str:key>/', PassReveal.as_view(), name='pass_reveal'),
        path('login/', Login.as_view(), name='login'),
        path('logout/', Logout.as_view(), name='logout'),
        path('signup/', Signup.as_view(), name='signup'),
]
