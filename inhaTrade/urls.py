from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # accounts 앱의 urls.py를 참조
    path('freights/', include('freights.urls')), # freight 앱의 urls.py를 참조
    path('quotes/', include('quotes.urls')),     # quotes 앱의 urls.py를 참조
]
