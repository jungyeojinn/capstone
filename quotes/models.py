from django.db import models
from django.conf import settings
from freights.models import Freight

class Quote(models.Model):
    id = models.AutoField(primary_key=True)                 #견적의 id는 자동으로 생성됨
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 견적을 등록한 사용자의 id. 사용자 삭제시 화물도 삭제
    freightId = models.ForeignKey(Freight, on_delete=models.CASCADE)                # 견적의 대상인 화물의 id. 화물 삭제시 견적도 삭제
    shippingCompany = models.CharField(max_length=50)       #운송사 이름
    totalCharge = models.CharField(max_length=50)
    departureDate = models.CharField(max_length=50)         #원하는 출발일
    arrivalDate = models.CharField(max_length=50)           #원하는 도착일
    isFCL = models.BooleanField(default=False)              #FCL 여부
    content = models.TextField()                            #메모
    
    created_at = models.DateTimeField(auto_now_add=True)    #견적 정보 등록 시간
    updated_at = models.DateTimeField(auto_now=True)        #견적 정보 수정 시간
    isAccepted = models.BooleanField(default=False)         #견적이 수락되었는지 여부
    
    class Meta:
        ordering = ['-created_at']