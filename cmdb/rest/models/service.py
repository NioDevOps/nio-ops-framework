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

    def save(self, *args, **kwargs):
        if self.pk:
            self.tree_path_cache = self.path()
        else:
            self.tree_path_cache = self.path(new=True)
        super(BaseService, self).save(*args, **kwargs)

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = "Tree node"
        verbose_name_plural = "Tree nodes"

    def path(self, new=False):
        p = [""]
        if new:
            s = self
            while s.parent:
                p.append(s.name)
                s=s.parent
            p.append(self.name)
            return '/'.join(p)

        for x in self.get_ancestors(ascending=False, include_self=False):
            p.append(x.name)
        p.append(self.name)
        return '/'.join(p)


class NormalService(BaseService):
    git = models.CharField(max_length=255)
    resources = models.ManyToManyField(BaseResource, blank=True)
    objects = PolymorphicManager()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = "normal-service"
        verbose_name_plural = "normal-services"


class MysqlService(BaseService):
    dbs = models.ManyToManyField(Db)
    objects = PolymorphicManager()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = "db-service"
        verbose_name_plural = "db-services"