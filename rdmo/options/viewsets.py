from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission

from .models import OptionSet, Option
from .serializers.v1 import (
    OptionSetSerializer,
    OptionSerializer,
    OptionSetIndexSerializer,
    OptionIndexSerializer,
    OptionSetNestedSerializer
)


class OptionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )

    @list_route()
    def nested(self, request):
        serializer = OptionSetNestedSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @list_route()
    def index(self, request):
        serializer = OptionSetIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class OptionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Option.objects.order_by('order')
    serializer_class = OptionSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )

    @list_route()
    def index(self, request):
        serializer = OptionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
