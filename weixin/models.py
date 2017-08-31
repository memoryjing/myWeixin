from django.db import models

# Create your models here.

class Order(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber=models.CharField(null=True,max_length=20,blank=True)
    goodsName = models.CharField(max_length=50)
    count = models.CharField(max_length=10)
    createTime=models.DateTimeField(null=True,blank=True)
    
    class Meta:
        ordering=("-createTime",)
        
        
