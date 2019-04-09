from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
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


class StepDefineViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = StepDefine.objects.all()
    serializer_class = StepDefineSerializer
    filter_backends = (OrderingFilter,)


class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.JWTAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = WorkflowTemplate.objects.all()
    serializer_class = WorkflowTemplateSerializer
    filter_backends = (OrderingFilter,)