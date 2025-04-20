from django import forms
from django.core.exceptions import ValidationError

from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ("title", "description", "image", "category", "condition")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ("ad_receiver", "comment")

    def __init__(self, *args, ad_sender=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ad_sender = ad_sender

        if ad_sender:
            own_ads = Ad.objects.filter(user=ad_sender.user) \
                .exclude(pk=ad_sender.pk)
            self.fields["ad_receiver"].queryset = own_ads

        # переключаем на радиокнопки
        self.fields["ad_receiver"].widget = forms.RadioSelect(
            attrs={"class": "form-check-input"}
        )
        # bootstrap‑класс для textarea
        self.fields["comment"].widget.attrs.update({"class": "form-control"})

    def clean_ad_receiver(self):
        receiver = self.cleaned_data.get("ad_receiver")
        if self.ad_sender and receiver == self.ad_sender:
            raise ValidationError("Нельзя предлагать обмен самому себе.")
        return receiver
