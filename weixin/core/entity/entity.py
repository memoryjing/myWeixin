

#实体类

from django.db import models

#商品
class Goods(models.Model):
    id=models.CharField(max_length=32)                  #
    name = models.CharField(max_length=30)              #商品名
    url= models.CharField(max_length=30)                #图片url，目前这个字段先不用
    description = models.CharField(max_length=50)       #描述
    create_time = models.CharField(max_length=30)       #商品添加时间
    last_modify_time = models.CharField(max_length=30)  #最后修改时间


#订单
class orders(models.Model):
    id = models.CharField(max_length=32)
    client_name= models.CharField(max_length=40)        #客户名称
    phone = models.EmailField(max_length=11)            #电话
    address = models.EmailField(max_length=60)          #地址
    remark = models.EmailField(max_length=100)          #备注
    create_time = models.EmailField(max_length=30)      #订单创建时间

#订单-商品列表
class orderGoods(models.Model):
    id = models.CharField(max_length=32)
    order_id = models.CharField(max_length=32)          #订单ID 外键
    goods_id = models.CharField(max_length=32)          #商品ID 外键
    weight = models.CharField(max_length=32)            #重量，单位：斤

