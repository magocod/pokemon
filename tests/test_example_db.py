"""
It was only set to test the successful connection in the database,
while no tests were created, delete later
"""

import pytest

from django.contrib.auth.models import User


pytestmark = [pytest.mark.django_db, pytest.mark.example]


def test_database_connection():
    """
    - test connection travis, docker, etc
    """

    # print('credentials', api_user._credentials)
    count = User.objects.count()
    assert count == User.objects.count()
