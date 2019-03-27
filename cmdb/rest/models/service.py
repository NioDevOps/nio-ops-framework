from mptt.models import MPTTModel, TreeForeignKey
from .base import *
from .resources import *
from django_extensions.db.fields.json import JSONField


class BaseService(MPTTModel, BaseConcurrentModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=64)
    tree_path_cache = models.CharField(max_length=255)
    info = models.CharField(max_length=255)

    def tree(self):
        pass


class NormalService(BaseService):
    git = models.CharField(max_length=255)
    resources = models.ManyToManyField(BaseResource, blank=True)


class MysqlService(BaseService):
    dbs = models.ManyToManyField(Db)
