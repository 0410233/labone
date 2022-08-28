from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from user.models import *
from .signals import *

import logging
logger = logging.getLogger('django')


# @receiver(post_save, sender=InviteLog, dispatch_uid='on_invitelog_created')
# def on_invitelog_created(sender, instance: InviteLog, created, **kwargs):
#     """接收信号：推荐关系建立"""
#     if created:
#         try:
#             # logger.warning('===== 推荐关系建立后，检查社员任务 =====')
#             from member.models import Task
#             from member.utils import check_task_completion
#             check_task_completion(instance.user, Task.Kind.INVITE)
#         except Exception as e:
#             logger.error('===== 推荐关系建立后，检查社员任务时发生错误 =====')
#             logger.error(str(e))

#         try:
#             # logger.warning('===== 邀请成功后，发放奖励 =====')
#             from member.models import CreditLog
#             from setting.models import get_setting_value

#             credit = float(get_setting_value('credit_invite', 0))
#             if credit != 0:
#                 CreditLog.objects.get_or_create(
#                     user=instance.user,
#                     log_type=CreditLog.LogType.INVITE,
#                     remark='User.pk='+str(instance.user.pk),
#                     defaults={
#                         'credit': credit,
#                         'title': CreditLog.LogType.INVITE.label,
#                     },
#                 )

#         except Exception as e:
#             logger.error('===== 邀请成功后，发放奖励时发生错误 =====')
#             logger.error(str(e))
