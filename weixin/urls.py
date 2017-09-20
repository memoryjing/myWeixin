from django.conf.urls import url
from . import views

urlpatterns = [
#     url(r'^$', views.index),
#     url(r'^article/(?P<article_id>[0-9]+)$', views.article_page,name='page'),
#     url(r'^edit/(?P<article_id>[0-9]+)$', views.edit_page,name="edit"),
#     url(r'^edit/action$', views.edit_action,name="action"),
#     #ÅÀÊý¾ÝÒ³Ãæ
#     url(r'^main/$', views.main_page,name="main"),
#     url(r'^tags_page$', views.get_tags,name="get_tags"),
#     url(r'^listurl$', views.get_listurl,name="listurl"),
#     url(r'^get_infos$', views.get_infos,name="get_infos"),
#     url(r'^startSearchByUrl$', views.startsearchbyurl,name="startsearchbyurl"),
#     url(r'^startSearchByTags$', views.startsearchbytags,name="startsearchbytags"),
#     url(r'^historyTask', views.historyTask,name="historyTask"),
#     url(r'^imgsAll$', views.get_imgs_all,name="imgsAll"),
#     #µÇÂ¼×¢²á
#     url(r'^$', views.login, name='default'),
#     url(r'^login/$', views.login, name='login'),
#     url(r'^logout/$', views.logout, name='logout'),
#     url(r'^regist/$', views.regist, name='regist'),
#     url(r'^index/$', views.index, name='index'),
#     #´ÊÔÆ
#     url(r'^ciyun/$', views.ciyun, name='ciyun'),
#     url(r'^getciyun/$', views.getciyun, name='getciyun'),
    #Î¢ÐÅ
    url(r'^main/$', views.main, name='main'),
    url(r'^wx/$', views.weixin, name='weixin'),
    url(r'^order/$', views.order, name='order'),
    url(r'^order/create$', views.orderCreate, name='orderCreate'),
    url(r'^order/list$', views.orderList, name='orderList'),
    

]