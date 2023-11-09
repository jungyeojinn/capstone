from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger
schema_view = get_schema_view(
    openapi.Info(
        title="inhaTrade API",  #API 문서 제목
        default_version='v1',
        description="inhaTrade API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="yeojin9905@naver.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # accounts 앱의 urls.py를 참조
    path('freights/', include('freights.urls')), # freight 앱의 urls.py를 참조
    path('quotes/', include('quotes.urls')),     # quotes 앱의 urls.py를 참조
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)), # swagger
]
