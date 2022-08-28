from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "初始化配置"

    # 初始化配置
    def handle(self, *args, **options):
        from setting.models import UserSetting
        
        self.stdout.write("正在初始化配置 ...")

        # 添加配置项
        settings = [{
            'key': 'lesson_signin_points',
            'value': '10',
            'name': '课程签到积分',
            'group': UserSetting.Group.POINTS,
        }]

        for item in settings:
            _item = item.copy()
            key = _item.pop('key')
            UserSetting.objects.update_or_create(key=key, defaults=_item)

        # 删除配置信息
        keys = [item['key'] for item in settings]
        UserSetting.objects.exclude(key__in=keys).delete()

        self.stdout.write("初始化配置完成。")
