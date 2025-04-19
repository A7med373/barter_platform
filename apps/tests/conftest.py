import pytest
from django.urls import reverse
from ads.models import Ad


@pytest.fixture
def user(django_user_model, db):
    return django_user_model.objects.create_user(
        username="alice", password="pass"
    )


@pytest.fixture
def other_user(django_user_model, db):
    return django_user_model.objects.create_user(
        username="bob", password="pass"
    )


@pytest.fixture
def ad(user):
    return Ad.objects.create(
        user=user,
        title="Гитара Fender",
        description="Отличное состояние",
        category="Музыка",
        condition="used",
    )


@pytest.fixture
def other_ad(other_user):
    return Ad.objects.create(
        user=other_user,
        title="iPhone 13",
        description="Как новый",
        category="Электроника",
        condition="new",
    )


@pytest.fixture
def client_logged(client, user):
    client.login(username="alice", password="pass")
    return client