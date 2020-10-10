import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    populate the database
    """
    with django_db_blocker.unblock():
        call_command("default_db")
        call_command("chat_example_db")


@pytest.fixture
def admin_client():
    """
    basic user
    """

    client = APIClient()
    token, _ = Token.objects.get_or_create(user__username="basic_user")
    client.credentials(
        HTTP_AUTHORIZATION="Token " + token.key,
    )
    return client
