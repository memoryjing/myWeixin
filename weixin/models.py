# -*- coding: utf-8 -*-

from django.db import models

#数据的删除使用物理删除，，不用逻辑删除                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                


# Create your models here.
#测试用表
class Order(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber=models.CharField(null=True,max_length=20,blank=True)
    goodsName = models.CharField(max_length=50)
    count = models.CharField(max_length=10)
    createTime=models.DateTimeField(null=True,blank=True)
    
    class Meta:
        ordering=("-createTime",)
        
#商品
class Goods(models.Model):
    name = models.CharField(max_length=30,null=False)              #商品名
    url= models.URLField(null=True,blank=True)                #图片url，目前这个字段先不用
    description = models.CharField(max_length=200,null=True,blank=True)       #描述
    create_time = models.DateTimeField(null=True,blank=True)       #商品添加时间
    last_modify_time = models.DateTimeField(null=True,blank=True)  #最后修改时间
    
    class Meta:
        ordering=("-create_time",)


#订单
class orders(models.Model):
    client_name= models.CharField(max_length=30,null=False)        #客户名称
    phone = models.CharField(max_length=11,null=False)            #电话
    address = models.CharField(max_length=150,null=False)          #地址
    content = models.CharField(max_length=500,blank=True)          #备注  备注就是用户要填写的内容
    audioId=models.CharField(max_length=256,blank=True)
    create_time = models.DateTimeField(null=True,blank=True)      #订单创建时间
    time = models.IntegerField(null=True,blank=True)                     #? 不可空，数字，1,2,3
    open_id=models.CharField(max_length=100,null=True,blank=True)         # ？ open_id, 长度未定？ 不可空
    class Meta:
        ordering=("-create_time",)

#订单-商品列表
class orderGoods(models.Model):
    order_id = models.CharField(max_length=12,null=False)          #订单ID 外键
    goods_id = models.CharField(max_length=12,null=False)          #商品ID 外键
    weight = models.PositiveIntegerField(default=0,null=False)     #重量，单位：斤
        
        
