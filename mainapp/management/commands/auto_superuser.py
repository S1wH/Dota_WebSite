from django.core.management.base import BaseCommand
from users.models import MyUser


class Command(BaseCommand):
    help = "script that creates a superuser"

    def handle(self):
        MyUser.objects.filter(username="admin", is_superuser=True).delete()

        # Creating superuser
        print("\nCreating superuser...\n")
        superuser = MyUser.objects.create_user(
            username="admin",
            email="admin@admin.ru",
            password="admin123",
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        print(f"Superuser {superuser} successfully created\n")
        print(f"username is {superuser.username}")
        print("password is admin123\n")
