__all__ = ['resources', 'service', 'orgnazition']
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    name = models.CharField(u'中文名', max_length=32, blank=False, null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    leaders = models.ManyToManyField("User", related_name="leader_ships", default=[])


class User(AbstractUser):
    name = models.CharField(u'中文名', max_length=32, blank=False, null=False)
    departments = models.ManyToManyField(Department, related_name="members", blank=True)

    def expend_department_nodes(self):
        return self.departments.all().get_descendants(include_self=True)
