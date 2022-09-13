import json

from django.db import models
from django.contrib.auth.models import AbstractUser

from server.utils import get_file_path


# Create your models here.


class User(AbstractUser):
    """微信用户"""

    class Role(models.IntegerChoices):
        VISITOR = 0, '游客'
        MANAGER = 1, '管理员'
        STUDENT = 2, '学生'
        PARENT  = 3, '家长'
        TEACHER = 4, '老师'

    openid = models.CharField('小程序openid', max_length=50, unique=True, blank=True, null=True)
    unionid = models.CharField('微信unionid', max_length=50, unique=True, blank=True, null=True)
    session_key = models.CharField('小程序密钥', max_length=50, blank=True, null=True)
    wx_user_info = models.TextField('微信用户信息', blank=True, null=True, help_text='json格式')
    name = models.CharField('微信昵称', max_length=50, blank=True, null=True)
    avatar = models.ImageField('微信头像', upload_to=get_file_path, max_length=500, blank=True, null=True)
    gender = models.IntegerField('性别', default=0, choices=[(0, '未知'), (1, '男'), (2, '女')])
    birthday = models.DateField('生日', blank=True, null=True)
    role = models.SmallIntegerField('角色', blank=True, default=0, choices=Role.choices)

    referrer_id = models.BigIntegerField('推荐人id', blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(str(self.pk), self.get_name())

    def get_name(self):
        if self.name:
            return self.name
        try:
            wx_user_info = self.wx_user_info
            if wx_user_info:
                wx_info = json.loads(wx_user_info)
                return wx_info.get('nickname', '')
        except json.decoder.JSONDecodeError:
            pass
        return ''
        
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# class InviteLog(models.Model):
#     """邀请记录"""
    
#     referrer = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='+', verbose_name='邀请人id')
#     user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='+', verbose_name='被邀请人id')

#     created_at = models.DateTimeField('创建时间', auto_now_add=True)

#     def __str__(self):
#         return str(self.pk)

#     class Meta:
#         verbose_name = '邀请记录'
#         verbose_name_plural = verbose_name
