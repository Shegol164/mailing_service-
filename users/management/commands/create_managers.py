from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import User


class Command(BaseCommand):
    help = 'Creates manager group and adds permissions'

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name='Менеджеры')

        permissions = [
            'view_all_mailings', 'disable_mailing',
            'view_all_clients', 'view_all_messages'
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                manager_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {perm} not found'))

        self.stdout.write(self.style.SUCCESS('Manager group created with permissions'))