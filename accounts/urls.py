# accounts/urls.py
from django.urls import path
from accounts.views import (
    LoginView, 
    LogoutView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

