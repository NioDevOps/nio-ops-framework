from django_cryptography.fields import encrypt
from django_extensions.db.fields.json import JSONField
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from .base import *
from . import Department


class BaseResource(PolymorphicModel,BaseConcurrentModel):  #
    name = models.CharField(u'资源名', max_length=64, blank=False, null=False)
    departments = models.ManyToManyField(Department, default=[])
    objects = PolymorphicManager()


class Interface(models.Model):
    interface_type = (
        (1, 'ipv4'),
        (2, 'ipv6'),
        (3, 'host'),
        (4, 'url'),
    )
    resource = models.ForeignKey(BaseResource, on_delete=models.CASCADE, related_name='interfaces')
    type = models.IntegerField(choices=interface_type, null=False)
    address = models.CharField(max_length=64, null=False)


class Label(models.Model):
    resource = models.ForeignKey(BaseResource, on_delete=models.CASCADE, related_name='labels')
    k = models.CharField(u'k', max_length=64, blank=False, null=False)
    v = models.CharField(u'v', max_length=64, blank=False, null=False)

    class Meta:
        unique_together = ["resource", "k", "v"]
        index_together = ["resource", "k", "v"]

    def __unicode__(self):
        return '%s: %s' % (self.k, self.v)


class K8sCluster(BaseResource):
    admin_token = models.CharField(max_length=64, blank=False, null=False)


class Container(BaseResource):
    cpu = models.IntegerField()
    mem = models.IntegerField()
    replicas = models.IntegerField(default=3)
    k8s_cluster = models.ForeignKey(K8sCluster, on_delete=models.PROTECT)
    extra_args = JSONField(default={})


class ServerType(BaseConcurrentModel):
    name = models.CharField(u'机器类型', max_length=64, blank=False, null=False)


class Server(BaseResource):
    server_type = models.ForeignKey(ServerType, on_delete=models.PROTECT)


class DbInstance(BaseResource):
    manage_user = models.CharField(u'管理账户', max_length=64, blank=False, null=False)
    manage_password = encrypt(models.CharField(max_length=50))
    port = models.IntegerField(default=3306)
    base_resource = models.ForeignKey(BaseResource, null=True, on_delete=models.CASCADE, related_name="belong_resource")


class Db(BaseConcurrentModel):
    name = models.CharField(max_length=64, blank=False, null=False)
    db_instance = models.ForeignKey("DbInstance", on_delete=models.CASCADE)



