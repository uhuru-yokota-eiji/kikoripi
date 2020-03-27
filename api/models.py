from django.db import models


# Create your models here.
class TickInterval(models.Model):
    interval = models.IntegerField()

    @classmethod
    def update_interval(cls, interval):
        """intervalの更新
        無ければ新規作成

        Args:
            interval (int): interval(ms)
        """
        t = cls.objects.all().first()
        if t:
            t.interval = interval
            t.save()
        else:
            cls.objects.create(interval=interval)
