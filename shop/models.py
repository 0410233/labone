from django.db import models

from server.utils import get_file_path

# Create your models here.


class PointLog(models.Model):
    """积分日志"""

    class LogType(models.IntegerChoices):
        SIGNIN = 0, '签到'
        EXCHANGE = 1, '兑换商品'
        OTHER = 10, '后台调整'

    student = models.ForeignKey('member.Student', on_delete=models.CASCADE, verbose_name='学生')
    log_type = models.SmallIntegerField('积分类型', default=0, choices=LogType.choices)
    points = models.FloatField('积分')
    remark = models.CharField('备注', max_length=200, blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.student), str(self.points))

    class Meta:
        verbose_name = '积分日志'
        verbose_name_plural = verbose_name
        db_table = 'point_log'
        ordering = ('-created_at',)


class PointGoods(models.Model):
    """积分商品"""
    
    name = models.CharField('商品名', max_length=45)
    image = models.ImageField('商品图片', upload_to=get_file_path, max_length=500)
    price = models.FloatField('兑换所需积分')
    stock = models.IntegerField('库存', blank=True, default=99)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.pk), self.name)

    class Meta:
        verbose_name = '积分商品'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)
        db_table = 'point_goods'


class ExchangeLog(models.Model):
    """商品兑换日志"""

    student = models.ForeignKey('member.Student', on_delete=models.CASCADE, verbose_name='学生')
    goods = models.ForeignKey('shop.PointGoods', on_delete=models.CASCADE, verbose_name='商品')
    points = models.FloatField('积分')

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.student), str(self.goods))

    class Meta:
        verbose_name = '商品兑换日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)
        db_table = 'exchange_log'
