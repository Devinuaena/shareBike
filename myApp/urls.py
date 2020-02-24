from django.conf.urls import url,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^user/$', views.user, name="user"),
    url(r'^customer/$', views.customer, name="customer"),
    # url(r'^showbike/$', views.showbike, name="showbike"),
    url(r'^selectbike/$', views.selectbike, name="selectbike"),
    url(r'^brokenbike/$', views.brokenbike, name="brokenbike"),
    url(r'^returnbike/$', views.returnbike, name="returnbike"),
    url(r'^pay/$', views.pay, name="pay"),
    url(r'^userSetting/$', views.userSetting, name="userSetting"),
    url(r'^trackbike/$', views.trackbike, name="trackbike"),
    url(r'^fixbike/$', views.fixbike, name="fixbike"),
    url(r'^changelocation/$', views.changelocation, name="changelocation"),
    url(r'^adminManager/$', views.adminManager, name="adminManager")
]


urlpatterns += staticfiles_urlpatterns()
