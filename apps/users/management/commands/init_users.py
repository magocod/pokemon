from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


USERS = (
    {
        "username": "pedro",
        "email": "admin@django.com",
        "password": "123",
        "first_name": "pedro",
        "last_name": "...",
        "staff": True,
        "super": True
    },
    {
        "username": "basic_user",
        "email": "user@django.com",
        "password": "123",
        "first_name": "user",
        "last_name": "Generic",
        "staff": False,
        "super": False
    },
)


class Command(BaseCommand):
    """
    ...
    """

    def handle(self, *args, **options):
        """
        ...
        """

        for dict_user in USERS:
            user = User.objects.create_user(
                dict_user["username"], dict_user["email"], dict_user["password"]
            )
            user.first_name = dict_user["first_name"]
            user.last_name = dict_user["last_name"]
            user.is_staff = dict_user["staff"]
            user.is_superuser = dict_user["super"]
            user.save()
