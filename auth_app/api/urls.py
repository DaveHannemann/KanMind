from django.urls import path
from .views import RegisterView, LogoutView, LoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]