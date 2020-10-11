import uuid

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.core.management import call_command
from django.contrib.auth.models import User


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    populate the database
    """

    with django_db_blocker.unblock():
        # pass
        call_command("init_db")
        # don't call along with (init_db)
        # call_command("init_users") 


@pytest.fixture
def test_password():
   return 'strong_password'


@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user


@pytest.fixture
def get_or_create_token(db, create_user):
   user = create_user()
   token, _ = Token.objects.get_or_create(user=user)
   return token


@pytest.fixture
def api_client():
   return APIClient()


@pytest.fixture
def api_user(get_or_create_token):
   token = get_or_create_token
   api_client = APIClient()
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   return api_client
