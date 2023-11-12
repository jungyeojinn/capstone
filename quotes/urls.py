from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quotes.as_view()),
    path('accepted', views.accepted_quotes.as_view()),
]