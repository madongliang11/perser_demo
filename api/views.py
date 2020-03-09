import json

from django.shortcuts import render, HttpResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework import serializers

from api import models


class ParameVersion(object):

    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        return version


class UserView(APIView):

    def get(self, request, *args, **kwargs):
        # self.dispatch()
        # version = request._request.GET.get('version')
        # print(version)
        # version = request.query_params.get('version')
        # print(version)
        # 获取版本
        print(request.version)
        # 获取处理版本的对象
        print(request.versioning_scheme)
        # 反向生成url(基于rest framnework)
        url = request.versioning_scheme.reverse(viewname='uuu', request=request)
        print(url)
        # 反向生成url(基于django)
        url1 = reverse(viewname='uuu', kwargs={'version': 1})
        print(url1)
        return HttpResponse('用户列表')


class DjangoView(APIView):

    def post(self, request, *args, **kwargs):
        from django.core.handlers.wsgi import WSGIRequest
        print(type(request._request))
        return HttpResponse('POST和Body')


from rest_framework.parsers import JSONParser, FormParser


class ParserView(APIView):
    # 如果在setting.py中配置全局解析器，此处可不写
    # parser_classes = [JSONParser, FormParser, ]
    """
    parser_classes中加入
    JSONParser：表示只能解析请求头为Content-Type: application/json的数据
    FormParser：表示只能解析请求头为Content-Type: application/x-www-form-urlencoded的数据
    """

    def post(self, request, *args, **kwargs):
        '''
        允许用户发送JSON格式数据，即可以接受下面这种情况
            a、Content-Type: application/json
            b、{'name': 'alex', 'age':18}
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        """
        整体步骤：
        1、获取用户请求
        2、获取用户请求体
        3、获取用户请求头和parser_classes = [JSONParser, FormParser, ]中支持的请求头进行比较
        4、例如JSONParser中请求头支持，JSONParser对象去请求体中解析数据
        5、将解析的数据赋值给request.data
        """
        # self.dispatch()
        # 获取解析后的结果，去请求体中获取值
        print(request.data)
        return HttpResponse('ParserView解析器')


class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class RolesView(APIView):
    def get(self, request, *args, **kwargs):

        # 方式一（原生实现方式，不借助DRF序列器）
        # roles = models.Role.objects.all().values('id', 'title')
        # roles = list(roles)
        # ret = json.dumps(roles, ensure_ascii=False)

        # 方式二：对于[obj, obj, obj]
        # roles = models.Role.objects.all().all()
        # # many=True表示有多条数据
        # ser = RolesSerializer(instance=roles, many=True)
        # ret = json.dumps(ser.data, ensure_ascii=False)

        # 方式三：转换单个对象
        role = models.Role.objects.all().all().first()
        # many=False表示有一条数据
        ser = RolesSerializer(instance=role, many=False)
        # ser.data已经是转换完成后的结果
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


###################################继承serializers.Serializer#################################################


class UserInfoSerializer(serializers.Serializer):
    user_type1 = serializers.CharField(source='user_type')
    user_type_choices1 = serializers.CharField(source='get_user_type_display')
    username = serializers.CharField()
    password = serializers.CharField()
    gp = serializers.CharField(source='group.title')
    # rls = serializers.CharField(source='roles.all')
    rls = serializers.SerializerMethodField()  # 自定义显示,显示的内容为一个函数返回值（gte开头，该字段结尾的函数）

    def get_rls(self, row):
        role_obi_list = row.roles.all()
        ret = []
        for item in role_obi_list:
            ret.append({'id': item.id, 'title': item.title})
        return ret


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfoSerializer(users, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


 ###################################继承serializers.ModelSerializer#############################################


class UserInfofoSerializer(serializers.ModelSerializer):
    user_type1 = serializers.CharField(source='user_type')
    user_type_choices1 = serializers.CharField(source='get_user_type_display')
    rls = serializers.SerializerMethodField()  # 自定义显示,显示的内容为一个函数返回值（gte开头，该字段结尾的函数）

    class Meta:
        model = models.UserInfo
        # 直接按数据库中的字段显示
        # fields = "__all__"
        fields = ['id', 'username', 'password', 'user_type1', 'user_type_choices1', 'rls']

    def get_rls(self, row):
        role_obi_list = row.roles.all()
        ret = []
        for item in role_obi_list:
            ret.append({'id': item.id, 'title': item.title})
        return ret


class UserInfofoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfofoSerializer(users, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


