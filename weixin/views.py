# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpRequest
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator
from urllib.request import urlopen
from . import models
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt 
from wechat_sdk import WechatBasic
from wechat_sdk.messages import ImageMessage, TextMessage, VoiceMessage, EventMessage, \
    LocationMessage, ShortVideoMessage
from wechat_sdk import WechatConf
from wechat_sdk.lib.request import WechatRequest

from datetime import datetime,date
import json
import math



# Create your views here.
WEIXIN_TOKEN="lijingjing"
BASE_URL="http://www.tiaoliaopifawang.cn"
ACCESS_TOKEN="4VCTc4mzckXznk6L8dLo7QK6NVKy2Y70f2mG3XpynQGn_IK\
            k81hNioTpxNqu3wmlVGa0hn8-JdjvtpNHlY1pv0UCFXGu7zxf0NZCbflYN3cZUXgADASNQ"
APPID='wx09d2abcb1236f865'
APPSECRET='720546183b347b96917a7408a27e8418'
#自定义菜单
MENU_DATA = {
        'button':[
        {
            'type': 'view',
            'name': '在线下单',
            'key': 'V1001_YUGOU',
            #'url':'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx09d2abcb1236f865&redirect_uri=https://www.tiaoliaopifawang.cn&response_type=code&scope=snsapi_base&state=1#wechat_redirect' 
            'url':'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx09d2abcb1236f865&redirect_uri=https://www.tiaoliaopifawang.cn/#/weixin/wx&response_type=code&scope=snsapi_base&state=1#wechat_redirect' 
            #BASE_URL+'/weixin/code/'
        },
        {
            'type': 'click',
            'name': '测试键',
            'key': 'V1001_TODAY_SINGER'
        },
        {
            'name': '个人中心',
            'sub_button': [
                {
                    'type': 'click',
                    'name': '我的订单',
                    'key': 'getOrderByOpenId'
                },
                {
                    'type': 'click',
                    'name': '取消今日订单',
                    'key': 'cancelOrder'
                },
                {
                    'type': 'view',
                    'name': '视频',
                    'url': 'http://v.qq.com/'
                },
                {
                    'type': 'click',
                    'name': '测试键',
                    'key': 'V1001_GOOD'
                }
            ]
        }
    ]
    }


def main(request):
    
    return render(request,"weixin/main.html")

def orderList(request):
    orders=models.Order.objects.all()
    return render(request,"weixin/orderList.html",{"orders":orders})

def initOrderForm(request):
    print("进入的是init函数")
    code_get=request.GET.get("code")
    print("获取到的code: "+str(code_get))
    url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+APPID+'&secret='+APPSECRET+'&code='+str(code_get)+'&grant_type=authorization_code'
    xml=urlopen(url).read().decode("utf8")
    doc=json.loads(xml)
    open_id=doc.get("openid")
    if open_id is None:
        open_id="orAO40mRn5-WbO8d10FWwLp4g67I"
    print("我终于拿到了openid"+str(open_id))
    orderList=models.orders.objects.filter(open_id=open_id,create_time__startswith=date.today())
    print(orderList)
    response_data={}
    data={}
    data["open_id"]=str(open_id);
    response_data["code"]="100000"
    response_data["msg"]="success"
    if len(orderList)>=1:
        order=orderList[0]
        data["client_name"]=order.client_name
        data["phone"]=order.phone
        data["address"]=order.address
        data["content"]=order.content   
    elif len(orderList)==0:
        data["client_name"]=""
        data["phone"]=""
        data["address"]=""
        data["content"]=""
    response_data["data"]=data
    return HttpResponse(json.dumps(response_data),content_type="application/json")
#     return HttpResponse(orderList[0].create_time)
@csrf_exempt
def saveOrder(request):
    response_data={}
    print(request.method)
    if request.method=="POST":
        formInfo=json.loads(request.POST.get("formInfo"))
        print(formInfo)
        client_name=formInfo.get("client_name")
        phone=formInfo.get("phone","")
        address=formInfo.get("address","")
        create_time=datetime.now()
        content=formInfo.get("content","")
        open_id=formInfo.get("open_id","")
        #判断数据库中是都已经存在该用户订单，根据openid
        order=models.orders.objects.filter(open_id=open_id,create_time__startswith=date.today())
        if(len(order)==0):
            time=1
            print("没有该用户的订单")
            models.orders.objects.create(client_name=client_name,phone=phone,address=address,create_time=create_time,
                                         content=content,open_id=open_id,time=time)
            response_data["code"]="100000"
            msg="第"+str(time)+"次创建订单成功"
            response_data["msg"]=msg
        else:
            time=order[0].time
            if time>=3:
                response_data["code"]="100001"
                msg="创建订单失败，每天最多三个订单"
                print(msg)
                print(type(msg))
                response_data["msg"]=msg
            else:
                time=time+1
                models.orders.objects.filter(open_id=open_id,create_time__startswith=date.today())\
                            .update(client_name=client_name,phone=phone,address=address,create_time=create_time,
                                         content=content,open_id=open_id,time=time)
                response_data["code"]="100000"
                msg="第"+str(time)+"次创建订单成功"
                print(msg)
                response_data["msg"]=msg
    return HttpResponse(json.dumps(response_data),content_type="application/json")
@csrf_exempt
def getOrderByOpenId(request):
    open_id="orAO40mRn5-WbO8d10FWwLp4g67I"
    data=[]
    order=[]
    orders=models.orders.objects.filter(open_id=open_id);
    orderLen=len(orders)
    if(orderLen==0):
        msg="没有订单"
        return HttpResponse("您还没有订单信息，快快点击在线下单订货吧~")
    elif orderLen>3:
        orders=orders[0:3]
        msg="超过三个订单"
    else:
        msg="三个订单以下"
    print(msg)
    count=1
    data.append("最近的订单信息：（最多三个）")
    for item in orders:
        
        print(item.client_name)
        print(item.content)
        order.append("[订单序号"+str(count)+"]:")
        order.append("客户姓名："+str(item.client_name))
        order.append("电话："+str(item.phone))
        order.append("收货地址："+str(item.address))
        order.append("订单日期："+str(item.create_time))
        order.append("订单内容:"+str(item.content))
        append_str="\n".join(order)
        data.append(append_str)
        order=[]
        count=count+1
    return HttpResponse("\n".join(data))
@csrf_exempt 
def cancelOrder(request):
    open_id="orAO40mRn5-WbO8d10FWwLp4g67I"
    orders=models.orders.objects.filter(open_id=open_id,create_time__startswith=date.today())
    ordersLen=len(orders)
    if ordersLen==0:
        msg="您今天没有订单"
    else:
        models.orders.objects.filter(open_id=open_id,create_time__startswith=date.today()).delete()
        msg="取消订单成功"
    return HttpResponse(msg)

def getTenPage(request):
    orders=models.orders.objects.all()
    paginator=Paginator(orders,10)
    orderInPage=paginator.page(2)
    for order in orderInPage:
        print(order.id)
    return HttpResponse("success")


def listOrderByParams(request):
    response_data={}
    order_data=[]
    data={}
    order={}
    dateStart=request.GET.get("dateStart")
    dateEnd=request.GET.get("dateEnd")
    client_name=request.GET.get("client_name")
    phone=request.GET.get("phone")
    pageSize=int(request.GET.get("pageSize"))
    curPage=int(request.GET.get("curPage"))
    orders=models.orders.objects.filter(create_time__gt=dateStart,create_time__lt=dateEnd,client_name__contains=client_name,
                                        phone__contains=phone)
    allDataCount=len(orders)
    response_data["code"]="100000"
    response_data["msg"]="success"
    data["allDataCount"]=math.ceil(allDataCount/pageSize)
    if allDataCount==0:
        data["curPageData"]=order_data
    else:
        paginator=Paginator(orders,pageSize)
        orderInPage=paginator.page(curPage)
        for item in orderInPage:
            order["id"]=item.id
            order["client_name"]=item.client_name
            order["phone"]=item.phone
            order["address"]=item.address
            order["content"]=item.content
            order["create_time"]=str(item.create_time)
            order_data.append(order)
            print(order_data)
            order={}
        data["curPageData"]=order_data
    response_data["data"]=data
    return HttpResponse(json.dumps(response_data),content_type="application/json")
@csrf_exempt   
def weixin(request):
    #设置配置信息
    conf=WechatConf(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET,
           encrypt_mode='normal',access_token_expires_at=7200,access_token=ACCESS_TOKEN)
    wechat=WechatBasic(conf=conf)
    #验证服务器
    if wechat.check_signature(signature=request.GET.get('signature'), 
                              timestamp=request.GET.get('timestamp'), 
                              nonce=request.GET.get('nonce')):
        print("111")
        if request.method=='GET':
            print("是GET请求")
            rsp=request.GET.get('echostr','error')
        else:
            print("是POST请求")
            wechat.create_menu(menu_data=MENU_DATA)
            wechat.parse_data(request.body)
            message=wechat.get_message()
            print("message"+str(message))
            #自动回复图文消息
            if isinstance(message,TextMessage):
                content=message.content
                if content=="管理员登录":
                    return HttpResponse(wechat.response_text("http://www.tiaoliaopifawang.cn/#/search"))
                else:
                    return HttpResponse(wechat.response_text("请点击菜单栏操作"))
            
            #自定义菜单事件推送
            elif isinstance(message, EventMessage):
                if message.type=="subscribe":
                    rsp=wechat.response_text("欢迎关注我的微信公众号~\n在这里你可以轻松地下订单")
                if message.type=="unsubscribe":
                    rsp=wechat.response_text("这是取消关注事件")
                if message.type=="click":
                    print("到了click事件")
                    if message.key=="cancelOrder":
                        print("点击的是删除今日订单事件")
                        open_id=message.source
                        orders=models.orders.objects.filter(open_id=open_id,create_time__startswith=date.today())
                        ordersLen=len(orders)
                        if ordersLen==0:
                            msg="您今天还没有订单呢~"
                        else:
                            models.orders.objects.filter(open_id=open_id,create_time__startswith=date.today()).delete()
                            msg="您成功取消今日订单"
                        return HttpResponse(wechat.response_text(msg))
                    elif message.key=="getOrderByOpenId":
                        print("点击的是查询订单事件")
                        open_id=message.source
                        data=[]
                        order=[]
                        orders=models.orders.objects.filter(open_id=open_id);
                        orderLen=len(orders)
                        if(orderLen==0):
                            msg="没有订单"
                            return HttpResponse(wechat.response_text("您还没有订单信息，快快点击在线下单订货吧~"))
                        elif orderLen>3:
                            orders=orders[0:3]
                            msg="超过三个订单"
                        else:
                            msg="三个订单以下"
                        print(msg)
                        count=1
                        data.append("最近的订单信息：（最多三个）")
                        for item in orders:
                            
                            print(item.client_name)
                            print(item.content)
                            order.append("[订单序号"+str(count)+"]:")
                            order.append("客户姓名："+str(item.client_name))
                            order.append("电话："+str(item.phone))
                            order.append("收货地址："+str(item.address))
                            order.append("订单内容:"+str(item.content))
                            append_str="\n".join(order)
                            data.append(append_str)
                            order=[]
                            count=count+1
                        rsp=wechat.response_text("\n".join(data))
                    else:   
                        rsp=wechat.response_text("测试键~你的openid是："+str(message.source))
                if message.type=="view":
                    open_id=message.source;
                    print("view事件中的openid="+str(open_id))
                    rsp=wechat.response_text("自定义菜单跳转链接事件"+str(message.source))
            
            #自动回复其他消息
            else:
                wechat.response_text("请点击菜单栏操作")
    else:
        rsp=wechat.response_text('check error')
    return HttpResponse(rsp)
    
