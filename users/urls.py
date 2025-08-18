from django.urls import path
from .views import LoginVIew, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginVIew.as_view(), name='login'),
]