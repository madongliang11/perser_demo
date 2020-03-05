from django.shortcuts import render, HttpResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from django.urls import reverse


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
    parser_classes = [JSONParser, FormParser, ]
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
        #
        # 获取解析后的结果，去请求中获取值
        print(request.data)
        return HttpResponse('ParserView解析器')

