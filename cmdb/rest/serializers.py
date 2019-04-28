from django.contrib.auth.models import Group
from .models import *
from .models import User, Department
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups', 'departments')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects, required=False)
    leaders = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects, required=False)

    class Meta:
        model = Department
        fields = "__all__"


# class ServiceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = service.BaseService
#         fields = "__all__"


class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = resources.Label
        fields = ('k', 'v')


class ServerTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = resources.ServerType
        fields = "__all__"


class InterfaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = resources.Interface
        fields = ('type', 'address')


class ServerSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, required=False)
    interfaces = InterfaceSerializer(many=True, required=False)
    departments = serializers.PrimaryKeyRelatedField(many=True, queryset=Department.objects, required=False)

    class Meta:
        model = resources.Server
        fields = "__all__"

    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        interfaces = validated_data.pop('interfaces', [])
        departments = validated_data.pop('departments', [])
        r = resources.Server.objects.create(**validated_data)
        for x in departments:
            r.departments.add(x)
        resources.Label.objects.bulk_create([resources.Label(resource=r, **label) for label in labels])
        resources.Interface.objects.bulk_create(
            [resources.Interface(resource=r, **interface) for interface in interfaces])
        return r


class DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = resources.Db
        fields = "__all__"


class DbInstanceSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, required=False)
    interfaces = InterfaceSerializer(many=True, required=False)
    departments = serializers.PrimaryKeyRelatedField(many=True, queryset=Department.objects, required=False)

    class Meta:
        model = resources.DbInstance
        fields = "__all__"

    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        interfaces = validated_data.pop('interfaces', [])
        departments = validated_data.pop('departments', [])
        r = resources.DbInstance.objects.create(**validated_data)
        for x in departments:
            r.departments.add(x)
        resources.Label.objects.bulk_create([resources.Label(resource=r, **label) for label in labels])
        resources.Interface.objects.bulk_create(
            [resources.Interface(resource=r, **interface) for interface in interfaces])
        return r


class ResourceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        resources.Server: ServerSerializer,
        resources.DbInstance: DbInstanceSerializer,
    }
    labels = LabelSerializer(many=True, required=False)
    interfaces = InterfaceSerializer(many=True, required=False)
    departments = serializers.PrimaryKeyRelatedField(many=True, queryset=Department.objects, required=False)


class NormalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.NormalService
        fields = "__all__"


class DbServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.MysqlService
        fields = "__all__"


class ServiceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        service.MysqlService: DbServiceSerializer,
        service.NormalService: NormalServiceSerializer,
    }


