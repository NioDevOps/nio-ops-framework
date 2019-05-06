from django_cryptography.fields import encrypt
from django_extensions.db.fields.json import JSONField
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from simple_history.models import HistoricalRecords
from .base import *
from . import Department


class BaseResource(PolymorphicModel, BaseConcurrentModel):  #
    name = models.CharField(u'资源名', max_length=64, blank=False, null=False)
    departments = models.ManyToManyField(Department, default=[])
    objects = PolymorphicManager()


class Interface(models.Model):
    history = HistoricalRecords()
    interface_type = (
        ('ipv4', 'ipv4'),
        ('ipv6', 'ipv6'),
    )
    resource = models.ForeignKey(BaseResource, on_delete=models.CASCADE, related_name='interfaces')
    type = models.CharField(choices=interface_type, max_length=64, null=False)
    address = models.CharField(max_length=64, null=False)

    class Meta:
        unique_together = ["resource", "type", "address"]
        index_together = ["resource", "type", "address"]

    def __unicode__(self):
        return '%s: %s' % (self.type, self.address)

    def __eq__(self, obj):
        return str(self) == str(obj)


class Label(models.Model):
    history = HistoricalRecords()
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
    history = HistoricalRecords()
    cpu = models.IntegerField()
    mem = models.IntegerField()
    replicas = models.IntegerField(default=3)
    k8s_cluster = models.ForeignKey(K8sCluster, on_delete=models.PROTECT)
    extra_args = JSONField(default={})


class ServerType(BaseConcurrentModel):
    name = models.CharField(u'机器类型', max_length=64, blank=False, null=False)
    history = HistoricalRecords()

class Server(BaseResource):
    history = HistoricalRecords()
    server_type = models.ForeignKey(ServerType, on_delete=models.PROTECT)


class DbInstance(BaseResource):
    history = HistoricalRecords()
    manage_user = models.CharField(u'管理账户', max_length=64, blank=False, null=False)
    manage_password = encrypt(models.CharField(max_length=50, blank=False, null=False))
    port = models.IntegerField(default=3306)
    base_resource = models.ForeignKey(BaseResource, null=True, on_delete=models.CASCADE, related_name="belong_resource")


class Db(BaseResource):
    history = HistoricalRecords()
    user = models.CharField(u'管理账户', max_length=64, blank=False, null=False)
    password = encrypt(models.CharField(max_length=50, blank=False, null=False))
    extra_args = JSONField(default={})
    db_instance = models.ForeignKey("DbInstance", on_delete=models.CASCADE)



