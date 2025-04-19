import pytest
from django.urls import reverse
from ads.models import Ad


@pytest.mark.django_db
def test_ad_create_view(client_logged):
    url = reverse("ad_create")
    data = {
        "title": "Samsung TV",
        "description": "55 дюймов, 4K",
        "category": "Электроника",
        "condition": "used",
    }
    resp = client_logged.post(url, data, follow=True)
    assert resp.status_code == 200
    assert Ad.objects.filter(title="Samsung TV").exists()


@pytest.mark.django_db
def test_ad_update_only_author(client, client_logged, ad, other_user):
    # попытка чужого пользователя отредактировать объявление
    client.login(username="bob", password="pass")
    url = reverse("ad_edit", args=[ad.pk])
    resp = client.post(url, {"title": "Новый заголовок"})
    assert resp.status_code == 403 or resp.status_code == 404

    # автор успешно обновляет
    url = reverse("ad_edit", args=[ad.pk])
    resp = client_logged.post(
        url, {
            "title": "Обновлено автором",
            "description": ad.description,
            "category": ad.category,
            "condition": ad.condition,
        },
        follow=True,
    )
    ad.refresh_from_db()
    assert ad.title == "Обновлено автором"


@pytest.mark.django_db
def test_ad_search_filter(client_logged, ad, other_ad):
    url = reverse("ad_list") + "?q=Гитара"
    resp = client_logged.get(url)
    assert ad.title in resp.content.decode()
    assert other_ad.title not in resp.content.decode()

    url = reverse("ad_list") + "?category=Электроника"
    resp = client_logged.get(url)
    assert other_ad.title in resp.content.decode()
    assert ad.title not in resp.content.decode()