import pytest
from django.db import IntegrityError
from ads.models import ExchangeProposal


@pytest.mark.django_db
def test_exchange_proposal_unique(ad, other_ad):
    # первое «в ожидании» предложение сохраняется
    p1 = ExchangeProposal.objects.create(
        ad_sender=ad, ad_receiver=other_ad, comment="Меняемся?"
    )
    assert p1.status == "pending"

    # второе «pending» в ту же пару запрещено (unique_constraint)
    with pytest.raises(IntegrityError):
        ExchangeProposal.objects.create(
            ad_sender=ad, ad_receiver=other_ad, comment="Ещё раз"
        )

    # предложение на собственное объявление запрещено (check_constraint)
    with pytest.raises(IntegrityError):
        ExchangeProposal.objects.create(
            ad_sender=ad, ad_receiver=ad, comment="Сам с собой"
        )