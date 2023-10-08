from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]