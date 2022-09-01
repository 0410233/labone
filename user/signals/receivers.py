from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from user.models import *
from .signals import *

import logging
logger = logging.getLogger('django')

