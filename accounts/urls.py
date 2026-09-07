from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .api import AssetTypeViewSet, AssetViewSet, LocationViewSet, StatusViewSet


api_router = DefaultRouter()
api_router.register(r'assets', AssetViewSet, basename='api-assets')
api_router.register(r'asset-types', AssetTypeViewSet, basename='api-asset-types')
api_router.register(r'statuses', StatusViewSet, basename='api-statuses')
api_router.register(r'locations', LocationViewSet, basename='api-locations')

urlpatterns = [
    path('api/', include(api_router.urls)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('employees/', views.employees_list, name='employees'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    # Управление активами
    path('assets/', views.assets_list, name='assets'),
    path('assets/import/', views.asset_import_excel, name='asset_import_excel'),
    path('assets/import/template/', views.asset_import_template, name='asset_import_template'),
    path('assets/add/', views.asset_add, name='asset_add'),
    path('assets/inventory/', views.inventory_list, name='inventory_list'),
    path('assets/inventory/<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('assets/inventory/<int:pk>/complete/', views.inventory_complete, name='inventory_complete'),
    path('assets/<int:pk>/edit/', views.asset_edit, name='asset_edit'),
    path('assets/<int:pk>/delete/', views.asset_delete, name='asset_delete'),
    # Мои активы
    path('my-assets/', views.my_assets, name='my_assets'),
    path('my-assets/byod/', views.my_byod_resources, name='my_byod_resources'),
    path('my-assets/byod/<int:pk>/', views.my_byod_resource_detail, name='my_byod_resource_detail'),
    path('my-assets/<int:asset_id>/repair-request/', views.create_repair_request, name='create_repair_request'),
    # Запросы на ремонт
    path('repair-requests/', views.repair_requests_list, name='repair_requests'),
    path('repair-requests/<int:pk>/approve/', views.approve_repair_request, name='approve_repair_request'),
    path('repair-requests/<int:pk>/reject/', views.reject_repair_request, name='reject_repair_request'),
    # Мои запросы
    path('my-requests/', views.my_requests, name='my_requests'),
    # QR-код и детали актива
    path('assets/<int:pk>/qr/', views.asset_qr, name='asset_qr'),
    path('assets/<int:pk>/history/', views.asset_history, name='asset_history'),
    path('assets/<int:pk>/', views.asset_detail, name='asset_detail'),
    # Отчёты
    path('reports/', views.reports_list, name='reports'),
    path('action-log/', views.action_log, name='action_log'),
    path('reports/assets-by-employee/', views.report_assets_by_employee, name='report_assets_by_employee'),
    path('reports/assets-by-employee/export/excel/', views.export_report_assets_by_employee_excel, name='export_assets_by_employee_excel'),
    path('reports/assets-by-employee/export/pdf/', views.export_report_assets_by_employee_pdf, name='export_assets_by_employee_pdf'),
    path('reports/assets-by-department/', views.report_assets_by_department, name='report_assets_by_department'),
    path('reports/assets-by-department/export/excel/', views.export_report_assets_by_department_excel, name='export_assets_by_department_excel'),
    path('reports/assets-by-department/export/pdf/', views.export_report_assets_by_department_pdf, name='export_assets_by_department_pdf'),
    path('reports/inventory-session/', views.report_inventory_session, name='report_inventory_session'),
    path('reports/inventory-session/export/excel/', views.export_report_inventory_session_excel, name='export_inventory_session_excel'),
    path('reports/inventory-session/export/pdf/', views.export_report_inventory_session_pdf, name='export_inventory_session_pdf'),
]
