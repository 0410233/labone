import json

from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *



class UserLoginSerializer(serializers.Serializer):

    code = serializers.CharField(
        label= '小程序code',
        max_length=50,
        write_only=True,
        required=True,
        help_text="小程序login返回的code"
    )

    referrer_id = serializers.IntegerField(
        label= '推荐人id',
        write_only=True,
        required=False,
    )


class UserMobileModifySerializer(serializers.Serializer):

    encryptedData = serializers.CharField(
        label= '小程序加密数据',
        max_length=10000,
        write_only=True,
        required=True,
    )

    iv = serializers.CharField(
        label= '小程序初始向量',
        max_length=10000,
        write_only=True,
        required=True,
    )


class CreateWxUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'openid', "unionid", "session_key", "wx_user_info",
            "name", "avatar", "gender", "birthday",
        )


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', "name", "avatar", "gender", "birthday", "role"
        )


class UserSerializer(serializers.ModelSerializer):

    wx_user_info = serializers.SerializerMethodField()
    def get_wx_user_info(self, obj):
        wx_str = obj.wx_user_info
        dic = {}
        try:
            if wx_str and len(wx_str):
                dic = json.loads(wx_str)
        except json.decoder.JSONDecodeError:
            pass
        return dic

    class Meta:
        model = User
        fields = (
            'id', 'username', "openid", "unionid", 'is_active',
            "wx_user_info", "name", "avatar", "gender", "birthday",
            "role", 'date_joined', 'last_login',
        )
        read_only_fields = ('role',)



class UserPutSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=False,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message='手机号已经存在')]
    )

    def validate(self, attrs):
        if 'avatar1' in dict(attrs).keys():
            attrs['avatar'] = attrs['avatar1']
            del attrs['avatar1']
        return attrs

    class Meta:
        model = User
        fields = (
            'id', 'username', "openid", "unionid", "session_key", "wx_user_info",
            "name", "avatar", "gender", "birthday", "role", "referrer_id",
            'date_joined', 'last_login',
        )
        read_only_fields = ('date_joined', 'last_login', "openid", "unionid", "session_key", 'username', "role", )
