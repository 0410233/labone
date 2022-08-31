from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from teaching.models import StudentSignin
from .signals import *

import logging
logger = logging.getLogger('django')


@receiver(post_save, sender=StudentSignin, dispatch_uid='on_studentsignin_created')
def on_studentsignin_created(sender, instance: StudentSignin, created, **kwargs):
    """接收信号：学生签到"""
    
    if created:
        try:
            # logger.warning('===== 学生签到后，增加积分 =====')
            from shop.models import PointLog
            from setting.models import get_setting_value

            points = float(get_setting_value('signin_points', 10))
            PointLog.objects.get_or_create(
                student=instance.student,
                log_type=PointLog.LogType.SIGNIN,
                remark='Timetable.pk=%s'%str(instance.timetable.pk),
                defaults={'points': points},
            )
        except Exception as e:
            logger.error('===== 学生签到后，增加积分时发生错误 =====')
            logger.error(str(e))
