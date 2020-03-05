from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UserView.as_view(), name='uuu'),
    url(r'^(?P<version>[v1|v2]+)/django/$', views.DjangoView.as_view(), name='ddd'),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view()),
]
