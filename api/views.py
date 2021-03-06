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
        role = models.Role.objects.all().first()
        # many=False表示有一条数据
        ser = RolesSerializer(instance=role, many=False)
        # ser.data已经是转换完成后的结果
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


###################################继承serializers.Serializer#################################################


class UserInfoSerializer(serializers.Serializer):
    user_type1 = serializers.IntegerField(source='user_type')
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
    user_type1 = serializers.IntegerField(source='user_type')
    user_type_choices1 = serializers.CharField(source='get_user_type_display')
    gp = serializers.CharField(source='group.title')
    rls = serializers.SerializerMethodField()  # 自定义显示,显示的内容为一个函数返回值（gte开头，该字段结尾的函数）

    class Meta:
        model = models.UserInfo
        # 直接按数据库中的字段显示
        # fields = "__all__"
        fields = ['id', 'username', 'password', 'user_type1', 'user_type_choices1', 'rls', 'gp']

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


##################################### 自动序列化连表，使用depth字段也可实现多层展示 ####################################


class UserInSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_url_kwarg='pk', lookup_field='group_id')

    class Meta:
        model = models.UserInfo
        # 直接按数据库中的字段显示
        # fields = "__all__"
        fields = ['id', 'username', 'password', 'group', 'roles']
        depth = 1  # 深度展示层数（官方建议0-10层），当表格中某些字段使用ForeignKey或ManyToManyField时，depth的值，代表想深度展示的层数


class UserInView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        # 对象，Serializers类处理，self.to_representation
        # QuerySet，ListSerializer类处理，self.to_representation
        # 1、实例化，将数据封装到对象，先执行__new__，再执行__init__
        '''
        如果many=True，执行ListSerializer对象的构造方法；
        如果many=False，执行UserInSerializer对象的构造方法；
        '''
        ser = UserInSerializer(users, many=True, context={'request': request})
        # 2、调用对象的data属性
        # 执行ListSerializer中to_representation方法
        # 执行UserInSerializer，先执行Serializer中to_representation方法，循环执行UserInSerializer中所有需要序列化的字段，获取指定字段对应的值或对象
        # 如果是CharField或IntegerField获取的是值，如果HyperlinkedIdentityField获取的是对象，再分别执行各个子段对应的to_representation方法，
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class GroupViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserGroup
        # 直接按数据库中的字段显示
        fields = "__all__"


class GroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = models.UserGroup.objects.filter(pk=pk).first()
        ser = GroupViewSerializer(obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


################################ 数据校验、验证 #####################################################

class TitleValidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '标题必须是以%s开头' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class UserGroupSerializer(serializers.Serializer):
    # validators自定义验证规则
    title = serializers.CharField(error_messages={"required": "不能为空"}, validators=[TitleValidator('老男人'), ])

    # 验证的钩子函数
    # 可以返回值，也可抛出异常
    def validate_title(self, value):
        print(value)
        # from rest_framework import exceptions
        # raise exceptions.ValidationError('就是不通过')
        return value


class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):
        '''
        对提交的数据进行数据校验
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        # 获取提交的数据
        print(request.data)
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)
        return HttpResponse('提交数据')


############################################## 分页 ########################################################

from api.utils.serializers.pager import PagerSerializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

'''
根据页码进行分页(看第n页，每页显示n条数据)
'''


class MyPageNumberPagination(PageNumberPagination):

    # 每页显示数据
    page_size = 10
    # 获取URL参数中传入的页码key
    page_query_param = 'page'
    # 获取URL参数中设置的每页显示数据条数，默认为None,表示每页显示数据以page_size值为准
    page_size_query_param = 'size'
    # 最大支持的每页显示的数据条数
    max_page_size = 5


class Pager1View(APIView):

    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        pg = MyPageNumberPagination()

        # 在数据库中获取分页的数据
        pagers_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        ser = PagerSerializers(instance=pagers_roles, many=True)

        # response = pg.get_paginated_response(ser.data)
        # return response
        return Response(ser.data)


'''
根据位置和个数进行分页(在某个位置，向后查看n条数据)
'''


class MyLimitOffsetPagination(LimitOffsetPagination):

    # 默认每页显示的数据条数
    default_limit = 10
    # URL中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # URL中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显得条数
    max_limit = 6


class Pager11View(APIView):

    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        pg = MyLimitOffsetPagination()

        # 在数据库中获取分页的数据
        pagers_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        ser = PagerSerializers(instance=pagers_roles, many=True)

        # response = pg.get_paginated_response(ser.data)
        # return response
        return Response(ser.data)


'''
游标分页(只让看上一页和下一页)
'''


class MyCursorPagination(CursorPagination):
    # URL传入的游标参数
    cursor_query_param = 'cursor'
    # 默认每页显示的数据条数
    page_size = 10
    # 根据ID从大到小排列
    ordering = '-id'
    # URL传入的每页显示条数的参数
    page_size_query_param = 'size'
    # 每页显示数据最大条数
    max_page_size = 1000


class Pager111View(APIView):

    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        pg = MyCursorPagination()

        # 在数据库中获取分页的数据
        pagers_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        ser = PagerSerializers(instance=pagers_roles, many=True)

        response = pg.get_paginated_response(ser.data)
        return response


########################################################### 视图、路由 ######################################################

from rest_framework.generics import GenericAPIView


class View1View(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializers
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()  # models.Role.objects.all()
        # 分页
        pagers_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=pagers_roles, many=True)
        return Response(ser.data)


from rest_framework.viewsets import GenericViewSet


class View2View(GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializers
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()  # models.Role.objects.all()
        # 分页
        pagers_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=pagers_roles, many=True)
        return Response(ser.data)


from rest_framework.viewsets import ModelViewSet


class View3View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializers
    pagination_class = PageNumberPagination


class View4View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializers
    pagination_class = PageNumberPagination


class Group1View(ModelViewSet):
    queryset = models.UserGroup.objects.all()
    serializer_class = GroupViewSerializer
    pagination_class = PageNumberPagination


############################################################ 渲染器 #################################################
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer, HTMLFormRenderer


class TestView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]

    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all().first()

        # 创建分页对象f
        pg = MyCursorPagination()

        # 在数据库中获取分页的数据
        pagers_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        ser = PagerSerializers(instance=pagers_roles, many=True)

        return Response(ser.data)
