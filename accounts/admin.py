from django.contrib import admin
from .models import User

admin.site.register(User)   # 관리자 페이지에서 User 모델을 관리할 수 있도록 등록
