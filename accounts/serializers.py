from rest_framework import serializers

from .models import Asset, AssetType, Location, Status


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ('id', 'name', 'description')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name', 'description')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'description')


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            'id',
            'asset_name',
            'inventory_number',
            'serial_number',
            'asset_type',
            'status',
            'employee',
            'location',
            'purchase_date',
            'price',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_employee(self, employee):
        if employee is not None and not employee.is_active:
            raise serializers.ValidationError('Нельзя назначить неактивного сотрудника.')
        return employee