# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpRequest
from django.http.response import HttpResponseRedirect
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



# Create your views here.
WEIXIN_TOKEN="lijingjing"
BASE_URL="http://ee33cac6.ngrok.io"
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
            'url':'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx09d2abcb1236f865&redirect_uri=https://ee33cac6.ngrok.io/weixin/order&response_type=code&scope=snsapi_base&state=1#wechat_redirect' 
            #BASE_URL+'/weixin/code/'
        },
        {
            'type': 'click',
            'name': '商品信息',
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
                    'type': 'view',
                    'name': '视频',
                    'url': 'http://v.qq.com/'
                },
                {
                    'type': 'click',
                    'name': '赞一下我们',
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
#     code_get=request.GET.get("code");
#     print("获取到的code: "+str(code_get))
#     url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+APPID+'&secret='+APPSECRET+'&code='+code_get+'&grant_type=authorization_code'
#     xml=urlopen(url).read().decode("utf8")
#     doc=json.loads(xml)
#     open_id=doc.get("openid")
    open_id="orAO40mRn5-WbO8d10FWwLp4g67I"
#     print("我终于拿到了openid"+str(openid))
#     orderList=models.orders.objects.filter(open_id=open_id,create_time_startswith=datetime.date.today())
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
       
    response_data["data"]=data
    return HttpResponse(json.dumps(response_data),content_type="application/json")
#     return HttpResponse(orderList[0].create_time)
@csrf_exempt
def saveOrder(request):
    response_data={}
    print(request.method)
    if request.method=="GET":
#     if request.method=="POST":
        client_name=request.GET.get("client_name","Terry Zhang")
        phone=request.GET.get("phone","18840823411")
        address=request.GET.get("address","大连理工大学软件学院综合楼五楼")
        create_time=datetime.now()
        content=request.GET.get("content","大料 100斤")
        open_id=request.GET.get("open_id","orAO40mRn5-WbO8d10FWwLp4g67I")
#         client_name=request.POST.get("formInfo").get("client_name")
#         client_name=request.POST.get("client_name","lijingjing")
#         phone=request.POST.get("phone","18840824202")
#         address=request.POST.get("address","DLUT")
#         create_time=datetime.now()
#         content=request.POST.get("content","花椒 10")
#         open_id=request.POST.get("open_id","orAO40mRn5-WbO8d10FWwLp4g67I")
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
    orders=models.orders.objects.filter(open_id=open_id);
    orderLen=len(orders)
    if(orderLen==0):
        msg="没有订单"
    elif orderLen>3:
        orders=orders[0:3]
        msg="超过三个订单"
    else:
        msg="三个订单已下"
    print(msg)
    for order in orders:
        print(order.client_name)
        print(order.content)
        data.append(order.client_name)
        data.append(" ")
        data.append(order.content)
    return HttpResponse(data)
@csrf_exempt   
def weixin(request):
    #设置配置信息
    conf=WechatConf(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET,
           encrypt_mode='normal',access_token_expires_at=7200,access_token=ACCESS_TOKEN)
    wechat=WechatBasic(conf=conf)
    print(wechat)
    #验证服务器
    if wechat.check_signature(signature=request.GET.get('signature'), 
                              timestamp=request.GET.get('timestamp'), 
                              nonce=request.GET.get('nonce')):
        print("111")
        if request.method=='GET':
            rsp=request.GET.get('echostr','error')
        else:
            wechat.create_menu(menu_data=MENU_DATA)
            wechat.parse_data(request.body)
            message=wechat.get_message()
            print("message"+str(message))
            #自动回复图文消息
            if isinstance(message,TextMessage):
                articles=[{
                    'title':'第一条',
                    'description':u'这是第一条新闻',
                    'url': u'http://www.baidu.com/',
                    }, {
                        'title': u'第二条',
                        'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                        'url': u'http://www.baidu.com/',
                        }, {
                            'title': u'第三条',
                            'description': u'这是第一条新闻',
                            'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                            'url': u'http://www.baidu.com/',
                            }]
                rsp=wechat.response_news(articles)
            #自动回复图片消息
            elif isinstance(message, ImageMessage):
                rsp=wechat.response_image(message.media_id)
            #自动回复语音消息
            elif isinstance(message, VoiceMessage) or isinstance(message, ShortVideoMessage):
                rsp=wechat.response_voice(message.media_id)
            elif isinstance(message, LocationMessage):
                rsp=wechat.response_text("地理位置")
            #自定义菜单事件推送
            elif isinstance(message, EventMessage):
                if message.type=="subcribe":
                    rsp=wechat.response_text("这是关注事件"+str(message.key))
                if message.type=="unsubcribe":
                    rsp=wechat.response_text("这是取消关注事件")
                if message.type=="click":
                    print("到了click事件")
                    
                    if message.key=="getOrderByOpenId":
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
                        rsp=wechat.response_text(message.source)
                if message.type=="view":
                    open_id=message.source;
                    print("view事件中的openid="+str(open_id))
                    rsp=wechat.response_text("自定义菜单跳转链接事件"+str(message.source))
            
            #自动回复空消息
            else:
                rsp=wechat.response_none()
    else:
        rsp=wechat.response_text('check error')
    return HttpResponse(rsp)
    
