from django.contrib import admin
from .models import AssetType, Status, Location, Asset, RepairRequest, InventorySession, InventoryItem


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description')
    search_fields = ('name', 'address')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('inventory_number', 'asset_type', 'status', 'employee', 'location', 'purchase_date', 'price')
    list_filter = ('asset_type', 'status', 'location')
    search_fields = ('inventory_number', 'serial_number', 'description')
    list_select_related = ('asset_type', 'status', 'employee', 'location')


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ('asset', 'requester', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('asset__inventory_number', 'asset__asset_name', 'requester__username')
    list_select_related = ('asset', 'requester')
    readonly_fields = ('created_at',)


class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 0
    readonly_fields = ('asset', 'expected_employee', 'expected_location', 'expected_status', 'checked_by', 'checked_at')


@admin.register(InventorySession)
class InventorySessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'location', 'created_by', 'created_at', 'completed_at')
    list_filter = ('status', 'location', 'created_at')
    search_fields = ('title', 'notes')
    list_select_related = ('location', 'created_by')
    inlines = [InventoryItemInline]
