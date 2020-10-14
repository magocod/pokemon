import uuid

import pytest
from rest_framework.authtoken.models import Token

pytestmark = [pytest.mark.django_db, pytest.mark.app_users, pytest.mark.auth]


request_data = {"username": uuid.uuid4(), "password": "code_number"}


def test_user_login(api_client, django_user_model):

    user = django_user_model.objects.create_user(**request_data)

    response = api_client.post("/login/", request_data, format="json")

    tk = Token.objects.get(user_id=user.id)

    assert response.status_code == 200
    assert response.data["token"] == tk.key


def test_user_login_incorrect_password(api_client, django_user_model):

    django_user_model.objects.create_user(**request_data)

    invalid_request = {"username": uuid.uuid4(), "password": "invalid"}
    response = api_client.post("/login/", invalid_request, format="json")

    assert response.status_code == 400
    assert (
        response.data["non_field_errors"][0]
        == "Unable to log in with provided credentials."
    )


def test_user_login_without_providing_credentials(api_client):
    response = api_client.post("/login/")
    assert response.status_code == 400


def test_user_logout(api_user):
    response = api_user.post("/logout/")
    assert response.status_code == 200


def test_user_logout_without_authenticating(api_client):
    response = api_client.post("/logout/")
    assert response.status_code == 401
