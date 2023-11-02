from django.db import models
from django.conf import settings

class Freight(models.Model):
    id = models.AutoField(primary_key=True) # 화물의 id는 자동으로 생성됨
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 화물을 등록한 사용자의 id. 사용자 삭제시 화물도 삭제
    productName = models.CharField(max_length=50)
    width = models.CharField(max_length=50)     #가로
    depth = models.CharField(max_length=50)     #세로
    height = models.CharField(max_length=50)    #높이
    weight = models.CharField(max_length=50)    #중량
    quantity = models.CharField(max_length=50)  #수량
    departureDate = models.CharField(max_length=50) #원하는 출발일
    arrivalDate = models.CharField(max_length=50)   #원하는 도착일
    departurePlace = models.CharField(max_length=50)    #출발지
    arrivalPlace = models.CharField(max_length=50)      #도착지
    content = models.CharField(max_length=256)          #메모
    
    created_at = models.DateTimeField(auto_now_add=True)    #화물 정보 등록 시간
    updated_at = models.DateTimeField(auto_now=True)        #화물 정보 수정 시간
    isCompleted = models.BooleanField(default=False)        #화물 견적 작성이 완료되었는지 여부
    
    class Meta:
        ordering = ['-created_at']