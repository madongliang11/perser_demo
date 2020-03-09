from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UserView.as_view(), name='uuu'),
    url(r'^(?P<version>[v1|v2]+)/django/$', views.DjangoView.as_view(), name='ddd'),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/roles/$', views.RolesView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo/$', views.UserInfoView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfofo/$', views.UserInfofoView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userin/$', views.UserInView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$', views.GroupView.as_view(), name='gp'),
    url(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view()),
]
