# from mptt.models import MPTTModel, TreeForeignKey
# from .base import *
# from . import User
#
#
# class Department(MPTTModel, BaseConcurrentModel):
# 	name = models.CharField(u'中文名', max_length=32, blank=False, null=False)
# 	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
# 	members = models.ManyToManyField(User)
# 	leaders = models.ManyToManyField(User, related_name="leader_ships")


