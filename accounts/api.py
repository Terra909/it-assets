from django.db.models import Q
from rest_framework import permissions, viewsets

from .access import get_user_access
from .models import Asset, AssetType, Location, Status
from .serializers import (
    AssetSerializer,
    AssetTypeSerializer,
    LocationSerializer,
    StatusSerializer,
)


class AssetsApiPermission(permissions.BasePermission):
    # Управление активами доступны только авторизованным пользователям, которые имеют право управлять

    message = 'Недостаточно прав для работы с активами.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        access = get_user_access(request.user)
        if request.method in permissions.SAFE_METHODS:
            return access.can_view_assets()
        return access.can_manage_assets()


class ReferenceApiPermission(permissions.BasePermission):
    # Справочники доступны только авторизованным пользователям раздела активов

    message = 'Недостаточно прав для работы со справочниками активов.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        access = get_user_access(request.user)
        if request.method in permissions.SAFE_METHODS:
            return access.can_view_assets()
        return access.can_manage_assets()


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = (AssetsApiPermission,)

    def get_queryset(self):
        queryset = Asset.objects.select_related(
            'asset_type', 'status', 'employee', 'location'
        ).all()

        query = self.request.query_params.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(asset_name__icontains=query)
                | Q(inventory_number__icontains=query)
                | Q(serial_number__icontains=query)
                | Q(description__icontains=query)
            )

        for parameter, field in (
            ('type', 'asset_type_id'),
            ('status', 'status_id'),
            ('employee', 'employee_id'),
        ):
            value = self.request.query_params.get(parameter)
            if value:
                queryset = queryset.filter(**{field: value})

        return queryset


class AssetTypeViewSet(viewsets.ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer
    permission_classes = (ReferenceApiPermission,)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (ReferenceApiPermission,)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (ReferenceApiPermission,)