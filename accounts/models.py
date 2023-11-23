from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager # AbstractUser와 Group을 상속받아서 사용자 모델을 커스텀

class UserManager(BaseUserManager): #superuser 생성을 위한 클래스
    use_in_migrations = True

    def _create_user(self, userId, password, **extra_fields):
        if not userId:
            raise ValueError('The given userId must be set')
        user = self.model(userId=userId, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, userId, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(userId, password, **extra_fields)

    def create_superuser(self, userId, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(userId, password, **extra_fields)

class User(AbstractUser):
    username = None
    userId = models.CharField(max_length=20, unique=True, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    companyName = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    isForwarder = models.BooleanField(default=False)
    objects = UserManager()
    totalItems = models.IntegerField(default=0) # 사용자가 등록한 화물/견적의 총 개수
    USERNAME_FIELD = 'userId' # 로그인 시 사용할 필드를 지정
