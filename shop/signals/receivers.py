from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from shop.models import ExchangeLog, PointLog, PointReport
from .signals import *

import logging
logger = logging.getLogger('django')


@receiver(post_save, sender=ExchangeLog, dispatch_uid='on_exchangelog_created')
def on_exchangelog_created(sender, instance: ExchangeLog, created, **kwargs):
    """接收信号：兑换商品"""

    if created:
        try:
            # logger.warning('===== 兑换商品后，减少积分 =====')
            points = -1*float(instance.goods.price)
            PointLog.objects.get_or_create(
                student=instance.student,
                log_type=PointLog.LogType.EXCHANGE,
                remark='ExchangeLog.pk=%s'%str(instance.pk),
                defaults={'points': points},
            )
        except Exception as e:
            logger.error('===== 兑换商品后，减少积分时发生错误 =====')
            logger.error(str(e))


@receiver(post_save, sender=PointLog, dispatch_uid='on_pointlog_created')
def on_pointlog_created(sender, instance: PointLog, created, **kwargs):
    """接收信号：积分变动"""

    if created:
        try:
            # logger.warning('===== 积分变动后，更新积分统计 =====')
            from django.db.models import Sum
            from django.utils import timezone
            points_sum = PointLog.objects.filter(student=instance.student).aggregate(points_sum=Sum('points'))
            points = points_sum['points_sum'] or 0
            PointReport.objects.update_or_create(
                student=instance.student,
                defaults={'points': points, 'updated_at': timezone.now()},
            )
        except Exception as e:
            logger.error('===== 积分变动后，更新积分统计时发生错误 =====')
            logger.error(str(e))
