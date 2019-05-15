from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from .models import *
import json
from mptt.templatetags.mptt_tags import cache_tree_children
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework import permissions
# from rest_framework_simplejwt import authentication
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, NumberFilter
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from concurrency.fields import IntegerVersionField


class DepartmentReadFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user = request.user
        # admin用户不过滤
        if str(user) == 'admin':
            return queryset
        elif user.is_anonymous:
            return []
        depts = user.expend_department_nodes()
        return queryset.filter(departments__in=depts).distinct()


class ResourceAccessPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


def recursive_node_to_dict(node):
    result = {
        'id': node.pk,
        'title': node.name
    }
    if hasattr(node, 'polymorphic_ctype'):
        result['type'] = str(node.polymorphic_ctype)
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result


def get_tree_json(m, search=None):
    queryset = m.objects.all()
    if search:
        queryset = queryset.filter(name__contains=search)
    root_nodes = cache_tree_children(queryset)
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))
    return dicts


@require_http_methods(['GET'])
def query_service_tree(request):
    response = {}
    search = request.GET.get('search', None)
    tree = get_tree_json(service.BaseService, search)
    response['tree'] = tree
    return JsonResponse(response)


@require_http_methods(['GET'])
def query_department_tree(request):
    response = {}
    search = request.GET.get('search', None)
    tree = get_tree_json(Department, search)
    response['tree'] = tree
    return JsonResponse(response)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk
        })


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def expend_department_nodes(self, request, *args, **kwargs):
        u = self.get_object()
        serializer_context = {
            'request': request,
        }
        serializer = DepartmentSerializer(u.expend_department_nodes(), context=serializer_context, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = service.BaseService.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DepartmentReadFilterBackend, DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('name', 'departments', 'polymorphic_ctype', 'labels')
    search_fields = ('$name', '$departments__name', '$labels__k', 'labels__v')
    ordering_fields = ('name', '_ctime', '_mtime')

    @action(methods=['get'], detail=True)
    def path(self, request, *args, **kwargs):
        s = self.get_object()
        # serializer_context = {
        #     'request': request,
        # }
        # serializer = ServiceSerializer(s.path(), context=serializer_context, many=True)
        # return Response(serializer.data)
        response = {}
        response['result'] = s.path()
        return JsonResponse(response)


class NormalServiceViewSet(viewsets.ModelViewSet):
    """
    标准服务crud api.
    """
    queryset = service.NormalService.objects.all()
    serializer_class = NormalServiceSerializer
    filter_backends = [DepartmentReadFilterBackend]



class DbServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = service.DbService.objects.all()
    serializer_class = DbServiceSerializer
    filter_backends = [DepartmentReadFilterBackend]


class BaseResourceViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('name', 'departments', 'polymorphic_ctype', 'labels', 'interfaces')
    search_fields = ('$name', '$departments__name', '$labels__k', 'labels__v')
    ordering_fields = ('name', '_ctime', '_mtime')
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = service.BaseResource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [DepartmentReadFilterBackend]

    def get_queryset(self):
        rt = self.request.query_params.get('resourcetype', None)
        service_pk = self.kwargs.get('service_pk', None)
        if service_pk:
            queryset = service.BaseService.objects.get(pk=service_pk).resources
        else:
            queryset = service.BaseResource.objects
        if rt is not None:
            o = getattr(resources, rt)
            queryset = queryset.instance_of(o).all()
        else:
            queryset = queryset.all()

        return queryset

    @action(methods=['get'], detail=True)
    def associate(self, request, *args, **kwargs):
        r = self.get_object()
        s_pk_from_param = self.request.query_params.get('service_pk')
        s_pk_from_path = self.kwargs.get('service_pk', None)
        s_pk = s_pk_from_path if s_pk_from_path else s_pk_from_param
        v = self.request.query_params.get('version')
        s = service.BaseService.objects.get(pk=s_pk)
        relate, _ = service.ServiceResourcesRelation.objects.get_or_create(resource=r, service=s)
        if relate.version != v:
            relate.version = v
            relate.save()
        return JsonResponse({'success': True})


class ServerViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = resources.Server.objects.all()
    serializer_class = ServerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('name', 'departments', 'polymorphic_ctype', 'labels', 'interfaces')
    search_fields = ('$name', '$departments__name', '$labels__k', 'labels__v')
    ordering_fields = ('name', '_ctime', '_mtime')
    filter_backends = (OrderingFilter,)
    #filter_backends = [DepartmentReadFilterBackend]
# def get_queryset(self):
# 	user = self.request.user
# 	if user.is_anonymous:
# 		return []
# 	else:
# 		depts = user.expend_department_nodes()
# 		queryset = self.queryset.filter(departments__in=depts)
# 	return queryset.distinct()


class DbInstanceViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = resources.DbInstance.objects.all()
    serializer_class = DbInstanceSerializer


class DbViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = resources.Db.objects.all()
    serializer_class = DbSerializer


class ServerTypeViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = resources.ServerType.objects.all()
    serializer_class = ServerTypeSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class MineViewSet(APIView):

    def get(self, request):
        user = self.request.user
        serializer_context = {
            'request': request,
        }
        serializer = UserSerializer(user, context=serializer_context)
        return Response(serializer.data)
