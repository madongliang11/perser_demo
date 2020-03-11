from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'view4', views.View4View)
router.register(r'group1', views.Group1View)

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
    url(r'^(?P<version>[v1|v2]+)/pager1/$', views.Pager1View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/pager11/$', views.Pager11View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/pager111/$', views.Pager111View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/view1/$', views.View1View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/view2/$', views.View2View.as_view({'get': 'list'})),

    # http://127.0.0.1:8000/api/v1/view3/?format=json
    url(r'^(?P<version>[v1|v2]+)/view3/$', views.View3View.as_view({'get': 'list', 'post': 'create'})),
    # http://127.0.0.1:8000/api/v1/view3.json
    url(r'^(?P<version>[v1|v2]+)/view3\.(?P<format>\w+)$', views.View3View.as_view({'get': 'list'})),
    # http://127.0.0.1:8000/api/v1/view3/1/?format=json
    url(r'^(?P<version>[v1|v2]+)/view3/(?P<pk>\d+)$', views.View3View.as_view(
        {'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
    # http://127.0.0.1:8000/api/v1/view3/1.json
    url(r'^(?P<version>[v1|v2]+)/view3/(?P<pk>\d+)\.(?P<format>\w+)$', views.View3View.as_view(
        {'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),

    url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
    url(r'^(?P<version>[v1|v2]+)/test/$', views.TestView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/test\.(?P<format>\w+)$', views.TestView.as_view()),
]
