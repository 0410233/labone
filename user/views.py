import os
from datetime import datetime
import requests
import json
import random

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Q, Count
from django.db.models.query import QuerySet
from django.conf import settings
from django.http import Http404, HttpRequest

from rest_framework import mixins, generics, status, permissions, views
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from server.WXBizDataCrypt import WXBizDataCrypt

import urllib.request
from .models import get_file_path

from server.utils import DEFAULT_RESPONSES
from .serializers import *

# Create your views here.


class UserLogin(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    login_response = openapi.Response('response description', UserSerializer)


    @swagger_auto_schema(
        operation_summary='用户登录',
        # operation_description='我是說明',
        responses={
            status.HTTP_201_CREATED: login_response,
            status.HTTP_400_BAD_REQUEST: '业务异常，具体message提示。', status.HTTP_401_UNAUTHORIZED: '系身份验证失败（token过期或非法账号）',
            status.HTTP_403_FORBIDDEN: '没权限', status.HTTP_404_NOT_FOUND: '请求路径不存在', status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: '客户发送的请求大小超过了2MB限制。',
            status.HTTP_500_INTERNAL_SERVER_ERROR: '系统内部异常', status.HTTP_502_BAD_GATEWAY: '网关异常'
        },
        tags=['用户'],
    )

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appid = settings.WX_APPID
        secret = settings.WX_SECRET

        code = request.data['code']

        resp = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                            {"appid": appid, 'secret': secret,
                             'js_code': code, 'grant_type': 'authorization_code'})
        data = json.loads(resp.text)

        if 'errcode' in dict(data).keys():
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = None
            if 'unionid' in dict(data).keys():
                try:
                    user = User.objects.get(unionid=data['unionid'])
                except User.DoesNotExist:
                    user = None
            if user is None:
                try:
                    user = User.objects.get(openid=data['openid'])
                except User.DoesNotExist:
                    user = None

            if user:
                if user.openid is None:
                    user.openid = data['openid']

                if user.unionid is None and 'unionid' in dict(data).keys():
                    user.unionid = data['unionid']

                user.session_key = data['session_key']

                serializer = UserSerializer(user, context={'request': request})
                token, _ = Token.objects.get_or_create(user=user)
                result = dict(serializer.data)
                result['token'] = token.key
                result['username'] = user.username

                user.session_key = data['session_key']

                now = timezone.now()
                if timezone.is_aware(now):
                    now = timezone.localtime(now)
                user.last_login = now

                user.save()

            else:
                seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
                sa = []
                for i in range(8):
                    sa.append(random.choice(seed))
                salt = ''.join(sa)
                data['username'] = salt

                dic = {'openid': data['openid'], 'session_key': data['session_key']}

                serializer = CreateWxUserSerializer(data=data, context={'request': request})

                if 'unionid' in dict(data).keys():
                    dic['unionid'] = data['unionid']
                if 'username' in dict(data).keys():
                    dic['username'] = data['username']

                result = {}

                if serializer.is_valid(raise_exception=True):
                    user = serializer.save(**dic)

                    token, _ = Token.objects.get_or_create(user=user)
                    result = UserSerializer(user, context={'request': request}).data
                    result['token'] = token.key
                    result['username'] = user.username
                    user.save()

            return Response(result, status=status.HTTP_201_CREATED)



class UserWxMobileModify(mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserMobileModifySerializer

    login_response = openapi.Response('response description', UserSerializer)

    @swagger_auto_schema(
        operation_summary='小程序用户修改手机号',
        # operation_description='我是說明',
        responses={
            status.HTTP_201_CREATED: login_response,
            status.HTTP_400_BAD_REQUEST: '业务异常，具体message提示。', status.HTTP_401_UNAUTHORIZED: '系身份验证失败（token过期或非法账号）',
            status.HTTP_403_FORBIDDEN: '没权限', status.HTTP_404_NOT_FOUND: '请求路径不存在', status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: '客户发送的请求大小超过了2MB限制。',
            status.HTTP_500_INTERNAL_SERVER_ERROR: '系统内部异常', status.HTTP_502_BAD_GATEWAY: '网关异常'
        },
        tags=['用户'],
    )

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        iv = request.data['iv']
        encryptedData = request.data['encryptedData']
        # try:
        appId = settings.WX_APPID

        sessionKey = self.request.user.session_key

        pc = WXBizDataCrypt(appId, sessionKey)

        data = pc.decrypt(encryptedData, iv)
        mobile = data['purePhoneNumber']

        try:
            user = User.objects.get(username=mobile)
            if user != self.request.user:
                raise ParseError('手机号已经存在')

        except User.DoesNotExist:
            user = request.user
            user.username = mobile
            user.save()

        # except:
        #     raise ParseError('未知错误')

        return Response(UserSerializer(request.user,context={"request":request}).data)



class UserDetail(mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.ListAPIView):

    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes =  (MultiPartParser, )
    pagination_class = None

    def get_queryset(self):
        queryset = User.objects.all()

        if self.request.method == 'POST':
            queryset = queryset.filter(pk=self.request.user.id)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserPutSerializer

        return UserSerializer

    @swagger_auto_schema(
        operation_summary='获取用户信息',
        manual_parameters= [
            openapi.Parameter('id', openapi.IN_PATH, description="", type=openapi.TYPE_INTEGER)
        ],
        responses=DEFAULT_RESPONSES,
        tags=['用户'],
    )
    def get(self, request: HttpRequest, *args, **kwargs):
        res = self.retrieve(request, *args, **kwargs)
        # user_info = res.data
        
        # 是否关注
        # res.data['is_fans'] = 0
        # if request.user.is_authenticated:
        #     pk = kwargs.get('pk', 0)
        #     fans_queryset = Fans.objects.filter(user=request.user, to_user__pk=int(pk))
        #     res.data['is_fans'] = 1 if fans_queryset.count() > 0 else 0

        return res

    @swagger_auto_schema(
        operation_summary='修改用户信息',
        responses=DEFAULT_RESPONSES,
        tags=['用户'],
    )
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        username = request.data.get('username')
        if username:
            user_list = User.objects.filter(username=username).exclude(id=pk)
            if len(user_list):
                raise ParseError('手机号已经存在')

        res = self.update(request, *args, **kwargs, partial=True)
        return res

    def update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        user = serializer.save()
        
        # 更新微信信息
        wx_user_info = self.request.data.get('wx_user_info', None)
        if type(wx_user_info) is str and len(wx_user_info) > 0:
            user.wx_user_info = wx_user_info
            user.save()

            try:
                user_info = json.loads(wx_user_info)

                # 下载图片到本地
                avatar = user_info['avatarUrl']
                filename = get_file_path(None, avatar)

                user.name = user_info['nickName']
                # user.sex = user_info['gender']
                user.save()

                if os.path.exists(settings.MEDIA_ROOT + '/'.join((filename.split('/')[:-1]))) is False:
                    os.makedirs(settings.MEDIA_ROOT + '/'.join((filename.split('/')[:-1])))

                urllib.request.urlretrieve(avatar, filename=settings.MEDIA_ROOT + filename)
                user.avatar = filename

                user.save()

                # # 邀请记录
                # if user.referrer_id and InviteLog.objects.filter(user=user).count() == 0:
                #     referrer = User.objects.filter(pk=int(user.referrer_id)).first()
                #     if referrer:
                #         InviteLog.objects.create(user=user, referrer=referrer)

            except json.decoder.JSONDecodeError:
                pass


class UserCurrentDetail(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    @swagger_auto_schema(
        operation_summary='获取当前用户信息',
        operation_description="""
            credit 积分
            is_active false时被冻结 
        """,
        responses=DEFAULT_RESPONSES,
        tags=['用户'],
    )
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=request.user.id)

        serializer = UserSerializer(user, context={'request': request})
        user_info = serializer.data

        return Response(user_info)
