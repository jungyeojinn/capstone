from django.db import models
from django.contrib.auth.models import AbstractUser, Group # AbstractUser와 Group을 상속받아서 사용자 모델을 커스텀

class User(AbstractUser):
    userId = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    userName = models.CharField(max_length=20)
    companyName = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    isForwarder = models.BooleanField(default=False)
