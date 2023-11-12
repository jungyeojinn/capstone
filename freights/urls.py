from django.urls import path
from . import views

app_name = 'freights'

urlpatterns = [
    path('', views.freight.as_view()),
    path('<int:freight_id>', views.freight_detail.as_view()),

]