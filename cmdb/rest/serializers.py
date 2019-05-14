from django.contrib.auth.models import Group
from .models import resources, service
from .models import User, Department
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class GroupsStringRelatedField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        g = Group.objects.filter(name=value)
        return g.get().pk


class UserSerializer(serializers.ModelSerializer):
    groups = GroupsStringRelatedField(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups', 'departments')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DepartmentSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects, required=False)
    leaders = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects, required=False)

    class Meta:
        model = Department
        fields = "__all__"


# resource serializer
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = resources.Label
        fields = ('k', 'v')


class ServerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = resources.ServerType
        fields = "__all__"


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = resources.Interface
        fields = ('type', 'address')


class AbResourceSerializer(serializers.ModelSerializer):
    """
        resource serializer
    """
    labels = LabelSerializer(many=True, required=False)
    interfaces = InterfaceSerializer(many=True, required=False)

    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        interfaces = validated_data.pop('interfaces', [])
        departments = validated_data.pop('departments', [])
        r = self.Meta.model.objects.create(**validated_data)
        r.departments.set(departments)
        r.interfaces.bulk_create(
            [resources.Interface(resource=r, **interface) for interface in interfaces])
        r.labels.bulk_create([resources.Label(resource=r, **label) for label in labels])
        return r

    def update(self, instance, validated_data):
        labels = validated_data.pop('labels', [])
        interfaces = validated_data.pop('interfaces', [])
        departments = validated_data.pop('departments', [])
        instance.__dict__.update(**validated_data)
        instance.departments.set(departments)
        instance.interfaces.all().delete()
        instance.interfaces.bulk_create(
            [resources.Interface(resource=instance, **interface) for interface in interfaces])
        instance.labels.all().delete()
        instance.labels.bulk_create([resources.Label(resource=instance, **label) for label in labels])
        instance.save()
        return instance


class ServerSerializer(AbResourceSerializer):

    class Meta:
        model = resources.Server
        fields = "__all__"


class DbSerializer(AbResourceSerializer):
    class Meta:
        model = resources.Db
        fields = "__all__"


class DbInstanceSerializer(AbResourceSerializer):
    labels = LabelSerializer(many=True, required=False)
    departments = serializers.PrimaryKeyRelatedField(many=True, queryset=Department.objects, required=True)

    class Meta:
        model = resources.DbInstance
        fields = "__all__"


class ResourceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        resources.Server: ServerSerializer,
        resources.Db: DbSerializer,
        resources.DbInstance: DbInstanceSerializer,
    }


# service serializer

class ServiceLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.ServiceLabel
        fields = ('k', 'v')


class AbServiceSerializer(serializers.ModelSerializer):
    """
    抽象service serializer
    """
    labels = ServiceLabelSerializer(many=True, required=False)

    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        departments = validated_data.pop('departments', [])
        r = self.Meta.model.objects.create(**validated_data)
        r.departments.set(departments)
        r.labels.bulk_create([service.ServiceLabel(service=r, **label) for label in labels])
        return r

    def update(self, instance, validated_data):
        labels = validated_data.pop('labels', [])
        departments = validated_data.pop('departments', [])
        instance.__dict__.update(**validated_data)
        instance.departments.set(departments)
        instance.labels.all().delete()
        instance.labels.bulk_create([service.ServiceLabel(service=instance, **label) for label in labels])
        instance.save()
        return instance


class NormalServiceSerializer(AbServiceSerializer):
    class Meta:
        model = service.NormalService
        fields = "__all__"


class DbServiceSerializer(AbServiceSerializer):
    class Meta:
        model = service.DbService
        fields = "__all__"


class ServiceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        service.DbService: DbServiceSerializer,
        service.NormalService: NormalServiceSerializer,
    }



