from django.contrib.auth.models import User


PRIVILEGED_GROUP_PERMISSION = 'accounts.manage_privileged_employees'
PRIVILEGED_VIEW_PERMISSION = 'accounts.view_privileged_employees'
ASSET_CARD_VIEW_PERMISSION = 'accounts.view_asset_card'
ASSET_HISTORY_VIEW_PERMISSION = 'accounts.view_asset_history'


class UserAccess:
    SECTION_PERMISSION_MAP = {
        'assets': ('accounts.view_assets_section', 'accounts.manage_assets_section'),
        'employees': ('accounts.view_employees_section', 'accounts.manage_employees_section'),
        'repair_requests': ('accounts.view_repair_requests_section', 'accounts.manage_repair_requests_section'),
        'reports': ('accounts.view_reports_section', 'accounts.manage_reports_section'),
        'action_log': ('accounts.view_action_log_section', 'accounts.manage_action_log_section'),
        'my_assets': ('accounts.view_my_assets_section', 'accounts.manage_my_assets_section'),
        'my_requests': ('accounts.view_my_requests_section', 'accounts.manage_my_requests_section'),
    }

    def __init__(self, user: User):
        self.user = user

    def get_primary_group(self):
        return self.user.groups.order_by('name').first()

    def get_primary_group_name(self):
        primary_group = self.get_primary_group()
        return primary_group.name if primary_group else ''

    def get_group_names(self):
        return list(self.user.groups.order_by('name').values_list('name', flat=True))

    def is_administrator(self):
        return (
            self.user.is_superuser
            or self.user.groups.filter(name='Администратор').exists()
            or self.user.has_perm('accounts.manage_privileged_employees')
        )

    def is_manager(self):
        return (
            not self.is_administrator()
            and self.user.groups.filter(name='Руководитель').exists()
        )

    def is_employee(self):
        return (
            self.user.groups.filter(name='Сотрудник').exists()
            or not (self.is_administrator() or self.is_manager())
        )

    def has_section_access(self, section_name):
        if self.user.is_superuser:
            return True
        view_perm, manage_perm = self.SECTION_PERMISSION_MAP.get(section_name, (None, None))
        return bool(view_perm and (self.user.has_perm(view_perm) or self.user.has_perm(manage_perm)))

    def has_full_section_access(self, section_name):
        if self.user.is_superuser:
            return True
        _, manage_perm = self.SECTION_PERMISSION_MAP.get(section_name, (None, None))
        return bool(manage_perm and self.user.has_perm(manage_perm))

    def can_view_assets(self):
        return self.has_section_access('assets')

    def can_manage_assets(self):
        return self.has_full_section_access('assets')

    def can_view_employees(self):
        return self.has_section_access('employees')

    def can_manage_employees(self):
        return self.has_full_section_access('employees')

    def can_view_repair_requests(self):
        return self.has_section_access('repair_requests')

    def can_manage_repair_requests(self):
        return self.has_full_section_access('repair_requests')

    def can_view_reports(self):
        return self.has_section_access('reports')

    def can_manage_reports(self):
        return self.has_full_section_access('reports')

    def can_view_action_log(self):
        return self.has_section_access('action_log')

    def can_manage_action_log(self):
        return self.has_full_section_access('action_log')

    def can_view_my_assets(self):
        return self.has_section_access('my_assets')

    def can_manage_my_assets(self):
        return self.has_full_section_access('my_assets')

    def can_view_my_requests(self):
        return self.has_section_access('my_requests')

    def can_manage_my_requests(self):
        return self.has_full_section_access('my_requests')

    def can_view_privileged_employees(self):
        if self.user.is_superuser:
            return True
        return self.user.has_perm(PRIVILEGED_VIEW_PERMISSION)

    def can_manage_privileged_employees(self):
        if self.user.is_superuser:
            return True
        return self.user.has_perm(PRIVILEGED_GROUP_PERMISSION)

    def can_view_asset_history(self):
        if self.user.is_superuser:
            return True
        return self.user.has_perm(ASSET_HISTORY_VIEW_PERMISSION)

    def can_view_asset_card(self):
        if self.user.is_superuser:
            return True
        return self.user.has_perm(ASSET_CARD_VIEW_PERMISSION)


def get_user_access(user: User) -> UserAccess:
    return UserAccess(user)