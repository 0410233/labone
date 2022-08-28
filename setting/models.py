from django.db import models
from server.utils import choices_to_str

# Create your models here.



class UserSetting(models.Model):
    """系统配置"""

    class Group(models.IntegerChoices):
        DEFAULT = 0, '未分组'
        POINTS = 1, '积分'
    
    key = models.CharField('key', max_length=50, unique=True)
    value = models.TextField('value', blank=True, null=True)
    name = models.CharField('名称', max_length=50)
    group = models.SmallIntegerField('分组', blank=True, default=Group.DEFAULT, choices=Group.choices, help_text=choices_to_str(Group))
    scope = models.SmallIntegerField('使用范围', blank=True, default=0, choices=[(0,'全部'),(1,'仅后端')], help_text='仅后端使用的配置项不会被前端获取到')
    display = models.IntegerField('显示顺序', blank=True, default=0, help_text='大的排前面')
    
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
        ordering = ('-display', 'id')
        db_table = 'user_settings'


def get_setting_value(key=None, default=None):
    """获取配置值"""
    if key is not None:
        record = UserSetting.objects.filter(key=key).first()
        if record and record.value is not None:
            return record.value
        return default
    queryset = UserSetting.objects.all()
    dic = {}
    for setting in queryset:
        dic[setting.key] = setting.value
    return dic


def get_settings(*keys, **kwargs):
    """获取配置值"""
    if len(keys) > 0:
        queryset = UserSetting.objects.filter(key__in=keys)
    else:
        queryset = UserSetting.objects.all()
    queryset = queryset.filter(**kwargs)
    result = {}
    for setting in queryset:
        result[setting.key] = setting.value
    return result



class SystemTaskLog(models.Model):
    """后台任务日志"""

    class TaskType(models.IntegerChoices):
        OTHER = 0, '其他'
    
    task_type = models.IntegerField('类型', default=TaskType.OTHER, choices=TaskType.choices)
    remark = models.CharField('备注', max_length=200, blank=True, null=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = '后台任务日志'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)
        db_table = 'system_task_log'


class Grade(models.Model):
    """年级"""

    name = models.CharField('年级', max_length='50')
    display = models.IntegerField('显示顺序', blank=True, default=0, help_text='大的靠前')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = '年级'
        verbose_name_plural = verbose_name
        db_table = 'grades'
        ordering = ('-display', 'created_at')
