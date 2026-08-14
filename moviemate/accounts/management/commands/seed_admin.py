from django.core.management.base import BaseCommand
from accounts.models import Customer
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Seeds initial admin and sample data'

    def handle(self, *args, **kwargs):
        admin, created = Customer.objects.get_or_create(
            email='admin@moviemate.com',
            defaults={
                'full_name': 'Super Admin',
                'mobile': '9999999999',
                'password': make_password('admin123'),
                'role': 'admin'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Successfully created admin account: admin@moviemate.com / admin123"))
        else:
            admin.role = 'admin'
            admin.save()
            self.stdout.write(self.style.SUCCESS("Ensured admin role for admin@moviemate.com"))
