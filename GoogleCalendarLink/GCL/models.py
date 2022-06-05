from django.db import models


# Create your models here.
class Event(models.Model):
    event_name = models.CharField(blank=False, null=False, max_length=200, verbose_name='عنوان رویداد')
    details = models.TextField(verbose_name='توضیحات')
    dates = models.DateTimeField(verbose_name='تاریخ رویداد')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='محل برگزاری')
    link = models.CharField(max_length=200, blank=True, null=True, verbose_name='لینک رویداد')
    is_all_day = models.BooleanField(default=None, verbose_name='رویداد روز کامل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = 'رویداد'
        verbose_name_plural = 'رویدادها'
