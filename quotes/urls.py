from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quotes.as_view()),
    path('accept', views.accept.as_view()),
]