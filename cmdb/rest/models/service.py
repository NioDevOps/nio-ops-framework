# from mptt.models import MPTTModel, TreeForeignKey
from .base import *
from .resources import *
from django_extensions.db.fields.json import JSONField
# from polymorphic.models import PolymorphicModel
# from polymorphic.managers import PolymorphicManager
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
# class AbBaseService(PolymorphicModel)

class BaseService(PolymorphicMPTTModel, BaseConcurrentModel):
    parent = PolymorphicTreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=64)
    tree_path_cache = models.CharField(max_length=255, blank=True,  null=True)
    info = models.CharField(max_length=255)

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = "Tree node"
        verbose_name_plural = "Tree nodes"

    def tree(self):
        pass


class NormalService(BaseService):
    git = models.CharField(max_length=255)
    resources = models.ManyToManyField(BaseResource, blank=True)
    objects = PolymorphicManager()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = "Normal Service"
        verbose_name_plural = "Normal Service"


class MysqlService(BaseService):
    dbs = models.ManyToManyField(Db)
    objects = PolymorphicManager()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = "Mysql Service"
        verbose_name_plural = "Mysql Service"