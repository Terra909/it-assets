from django.db import models
from django.contrib.auth.models import User


class AssetType(models.Model):
    #Тип актива (ноутбук, монитор, принтер и т.д.)
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Название типа')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Тип актива'
        verbose_name_plural = 'Типы активов'
        ordering = ['name']
        default_permissions = ()
    
    def __str__(self):
        return self.name


class Status(models.Model):
    #Статус актива (в использовании, в ремонте, списан и т.д.)
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Название статуса')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']
        default_permissions = ()
    
    def __str__(self):
        return self.name


class Location(models.Model):
   #Местоположение актива (офис, склад и т.д.)
    
    name = models.CharField(max_length=200, unique=True, verbose_name='Название локации')
    address = models.CharField(max_length=300, blank=True, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['name']
        default_permissions = ()
    
    def __str__(self):
        return self.name


class Asset(models.Model):
   #Модель IT-актива
    
    asset_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название актива'
    )
    inventory_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Инвентарный номер'
    )
    serial_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Серийный номер'
    )
    asset_type = models.ForeignKey(
        AssetType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип актива'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Статус'
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets',
        verbose_name='Сотрудник'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    purchase_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата покупки'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Цена'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        db_table = 'accounts_asset'
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'
        ordering = ['-created_at']
        default_permissions = ()
        permissions = (
            ('view_asset_card', 'Может просматривать карточку актива'),
            ('view_asset_history', 'Может просматривать историю актива'),
        )
    
    def __str__(self):
        return f"{self.inventory_number} - {self.asset_type}"


class RepairRequest(models.Model):
   #Запрос на ремонт актива
    
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        APPROVED = 'approved', 'Принят'
        REJECTED = 'rejected', 'Отклонён'
    
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='repair_requests',
        verbose_name='Актив'
    )
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='repair_requests',
        verbose_name='Заявитель'
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name='Статус запроса'
    )
    reason = models.TextField(
        blank=True,
        verbose_name='Причина запроса'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата обработки'
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_repair_requests',
        verbose_name='Обработал'
    )
    
    class Meta:
        db_table = 'accounts_repair_request'
        verbose_name = 'Запрос на ремонт'
        verbose_name_plural = 'Запросы на ремонт'
        ordering = ['-created_at']
        default_permissions = ()
    
    def __str__(self):
        return f"Запрос на ремонт {self.asset.inventory_number} - {self.get_status_display()}"


class ActionLog(models.Model):
   #Журнал действий пользователей в системе
    
    class ActionType(models.TextChoices):
        LOGIN = 'login', 'Авторизация'
        LOGOUT = 'logout', 'Выход'
        ASSET_CREATE = 'asset_create', 'Добавлен актив'
        ASSET_EDIT = 'asset_edit', 'Отредактирован актив'
        ASSET_DELETE = 'asset_delete', 'Удалён актив'
        ASSET_TRANSFER = 'asset_transfer', 'Передан актив'
        EMPLOYEE_CREATE = 'employee_create', 'Добавлен сотрудник'
        EMPLOYEE_EDIT = 'employee_edit', 'Отредактирован сотрудник'
        EMPLOYEE_DELETE = 'employee_delete', 'Удалён сотрудник'
        REQUEST_CREATE = 'request_create', 'Создан запрос на ремонт'
        REQUEST_APPROVE = 'request_approve', 'Принят запрос на ремонт'
        REQUEST_REJECT = 'request_reject', 'Отклонён запрос на ремонт'
        REPORT_CREATE = 'report_create', 'Создан отчёт'
        INVENTORY_CREATE = 'inventory_create', 'Создана инвентаризация'
        INVENTORY_COMPLETE = 'inventory_complete', 'Завершена инвентаризация'
        INVENTORY_CHECK = 'inventory_check', 'Отмечен результат инвентаризации'
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='action_logs',
        verbose_name='Пользователь'
    )
    action_type = models.CharField(
        max_length=30,
        choices=ActionType.choices,
        verbose_name='Тип действия'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание действия'
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='ID объекта'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время действия'
    )
    
    class Meta:
        db_table = 'accounts_action_log'
        verbose_name = 'Журнал действий'
        verbose_name_plural = 'Журналы действий'
        ordering = ['-created_at']
        default_permissions = ()
    
    def __str__(self):
        return f"{self.get_action_type_display()} - {self.user.username} - {self.created_at}"


class BYODResource(models.Model):
   #Личная техника сотрудника, используемая для рабочих задач.

    class ResourceType(models.TextChoices):
        LAPTOP = 'laptop', 'Личный ноутбук'
        PHONE = 'phone', 'Личный телефон'
        TABLET = 'tablet', 'Личный планшет'
        PC = 'pc', 'Домашний ПК'
        OTHER = 'other', 'Другое устройство'

    class UsageStatus(models.TextChoices):
        ACTIVE = 'active', 'Используется в работе'
        LIMITED = 'limited', 'Используется частично'
        PAUSED = 'paused', 'Временно не используется'
        RETIRED = 'retired', 'Больше не используется'

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='byod_resources',
        verbose_name='Сотрудник'
    )
    device_name = models.CharField(max_length=200, verbose_name='Название устройства')
    resource_type = models.CharField(
        max_length=20,
        choices=ResourceType.choices,
        default=ResourceType.OTHER,
        verbose_name='Тип ресурса'
    )
    brand_model = models.CharField(max_length=200, blank=True, verbose_name='Марка и модель')
    serial_number = models.CharField(max_length=100, blank=True, verbose_name='Серийный номер / ID')
    usage_status = models.CharField(
        max_length=20,
        choices=UsageStatus.choices,
        default=UsageStatus.ACTIVE,
        verbose_name='Статус использования'
    )
    work_purpose = models.CharField(max_length=255, verbose_name='Для каких рабочих задач используется')
    support_notes = models.TextField(
        blank=True,
        verbose_name='Ограничения поддержки и договорённости'
    )
    compensation_notes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Компенсация / договорённости'
    )
    is_company_approved = models.BooleanField(default=False, verbose_name='Согласовано компанией')
    employee_consent = models.BooleanField(default=False, verbose_name='Сотрудник подтвердил условия учёта')
    last_confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Последнее подтверждение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'accounts_byod_resource'
        verbose_name = 'BYOD-ресурс'
        verbose_name_plural = 'BYOD-ресурсы'
        ordering = ['-updated_at', '-created_at']
        default_permissions = ()

    def __str__(self):
        return f"{self.device_name} ({self.employee.username})"


class InventorySession(models.Model):
   #Сессия инвентаризации корпоративных активов.

    class StatusChoices(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        IN_PROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Завершена'

    title = models.CharField(max_length=200, verbose_name='Название инвентаризации')
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
        verbose_name='Статус'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Локация'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_inventory_sessions',
        verbose_name='Создал'
    )
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    notes = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'accounts_inventory_session'
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризации'
        ordering = ['-created_at']
        default_permissions = ()

    def __str__(self):
        return self.title


class InventoryItem(models.Model):
   #Строка инвентаризации по корпоративному активу.

    class ResultChoices(models.TextChoices):
        PENDING = 'pending', 'Не проверен'
        MATCHED = 'matched', 'Совпадает'
        MISMATCH = 'mismatch', 'Расхождение'
        MISSING = 'missing', 'Не найден'

    session = models.ForeignKey(
        InventorySession,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Инвентаризация'
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name='Актив'
    )
    expected_employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Ожидаемый сотрудник'
    )
    expected_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Ожидаемая локация'
    )
    expected_status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Ожидаемый статус'
    )
    actual_employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Фактический сотрудник'
    )
    actual_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Фактическая локация'
    )
    actual_status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Фактический статус'
    )
    result = models.CharField(
        max_length=20,
        choices=ResultChoices.choices,
        default=ResultChoices.PENDING,
        verbose_name='Результат'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    checked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checked_inventory_items',
        verbose_name='Проверил'
    )
    checked_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата проверки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'accounts_inventory_item'
        verbose_name = 'Строка инвентаризации'
        verbose_name_plural = 'Строки инвентаризации'
        ordering = ['asset__inventory_number']
        default_permissions = ()
        unique_together = ('session', 'asset')

    def __str__(self):
        return f"{self.session.title}: {self.asset.inventory_number}"
