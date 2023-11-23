from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)
#from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.permissions import IsAuthenticated
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login.as_view(), name='login'),
    path('detail/', views.detail, name='detail'),
]