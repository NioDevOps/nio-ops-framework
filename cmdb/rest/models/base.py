from django.db import models
from concurrency.fields import IntegerVersionField
from . import User


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     name = models.CharField(u'姓名', max_length=32, blank=False, null=False)
#
#     class Meta:
#         verbose_name = u'用户详情'
#         verbose_name_plural = u"用户详情"


class BaseConcurrentModel(models.Model):
	_version = IntegerVersionField()
	_ctime = models.DateTimeField(auto_now_add=True)
	_mtime = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True



