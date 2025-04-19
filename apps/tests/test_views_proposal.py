import pytest
from django.urls import reverse
from ads.models import ExchangeProposal


@pytest.mark.django_db
def test_proposal_create(client_logged, ad, other_ad):
    url = reverse("proposal_create", kwargs={"ad_id": ad.pk})
    data = {"ad_receiver": other_ad.pk, "comment": "Сделка?"}
    resp = client_logged.post(url, data, follow=True)

    assert resp.status_code == 200
    assert ExchangeProposal.objects.filter(
        ad_sender=ad, ad_receiver=other_ad
    ).exists()