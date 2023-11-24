from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quotes.as_view()),
    path('accept', views.accept.as_view()),
    path('<int:quote_id>', views.quote_detail.as_view()),
]