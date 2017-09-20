# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from . import models
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt 
from wechat_sdk import WechatBasic
from wechat_sdk.messages import ImageMessage, TextMessage, VoiceMessage, EventMessage, \
    LocationMessage, ShortVideoMessage
from wechat_sdk import WechatConf
from django.http import HttpRequest
from wechat_sdk.lib.request import WechatRequest
from datetime import datetime
from urllib.request import urlopen
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
                    'type': 'view',
                    'name': '我的订单',
                    'url': BASE_URL+'/weixin/main/'
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
@csrf_exempt
def orderCreate(request):
    print(request.method)
    if request.method=="POST":
        name=request.POST.get("name")
        telNumber=request.POST.get("telephoneNumber")
        goodsName=request.POST.get("goodsName")
        count=request.POST.get("count")
        createTime=datetime.now()
        models.Order.objects.create(name=name,phoneNumber=telNumber,
                                   goodsName=goodsName,count=count,createTime=createTime)
    return HttpResponse("创建订单成功")
def orderList(request):
    orders=models.Order.objects.all()
    return render(request,"weixin/orderList.html",{"orders":orders})

def order(request):
    code_get=request.GET.get("code");
    print("获取到的code: "+str(code_get))
    url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+APPID+'&secret='+APPSECRET+'&code='+code_get+'&grant_type=authorization_code'
    xml=urlopen(url).read().decode("utf8")
    doc=json.loads(xml)
    openid=doc.get("openid")
    print("我终于拿到了openid"+str(openid))
    return render(request,"weixin/order.html")

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
                    'description': '这是第一条新闻',
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
                    rsp=wechat.response_text("自定义菜单点击事件"+str(message.key)+" "+str(message.source))
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
    
