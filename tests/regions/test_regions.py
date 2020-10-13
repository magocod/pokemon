"""
These tests rely on the (load_regions) command to get data

call_command("load_regions")

Note: future versions will adjust these conditions
"""

import pytest

from django.urls import reverse

from apps.regions.models import Region
from apps.regions.serializers import RegionDetailSerializer, RegionSerializer

pytestmark = [pytest.mark.django_db, pytest.mark.app_regions, pytest.mark.regions]


def test_list_all_regions(api_client):
    url = reverse("regions_list")
    serializer = RegionSerializer(Region.objects.all(), many=True)
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == serializer.data


def test_get_region_detail(api_client):
    region_pk = 1
    serializer = RegionDetailSerializer(Region.objects.get(pk=region_pk))

    response = api_client.get(f"/regions/{region_pk}/")

    assert response.status_code == 200
    assert response.data == serializer.data


def test_get_region_not_found(api_client):
    response = api_client.get(f"/regions/{10000000000}/")

    assert response.status_code == 404
