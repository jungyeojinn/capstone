from django.db import models
from django.contrib.auth.models import AbstractUser, Group # AbstractUser와 Group을 상속받아서 사용자 모델을 커스텀

class User(AbstractUser):
    username = None
    userId = models.CharField(max_length=20, unique=True, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    companyName = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    isForwarder = models.BooleanField(default=False)
    USERNAME_FIELD = 'userId' # 로그인 시 사용할 필드를 지정
