from django.core.management import BaseCommand
from apps.account.models import User

class Command(BaseCommand):
    help = 'Create admin user'
    def handle(self, *args, **options):
        email = input('Enter email: ')
        role = input("Enter role: ").strip().lower()

        if role not in ['admin', 'god']:
            self.stdout.write(self.style.ERROR('Invalid role.(admin or god)'))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR('User already exists.'))
            return

        user = User.objects.create_user(email=email,role = User.Roles.ADMIN if role == 'admin' else User.Roles.GOD_USER)
        print(user)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created {role} user: {email}"))