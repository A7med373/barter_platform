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

    def __init__(self, *args, ad_sender=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ad_sender = ad_sender
        self.user = user

        if self.user and self.ad_sender:
            print("Initializing form with ad_sender:", ad_sender.id)  # Отладочная информация
            print("Current user:", user.username)  # Отладочная информация
            self.own_ads = Ad.objects.filter(user=self.user).exclude(pk=self.ad_sender.pk)
            print("Available ads:", self.own_ads.values_list('id', 'title'))  # Отладочная информация
            self.fields["ad_receiver"].queryset = self.own_ads
            self.fields["ad_receiver"].empty_label = None  # Убираем пустой вариант

        # bootstrap‑класс для textarea
        self.fields["comment"].widget.attrs.update({"class": "form-control"})
        self.fields["comment"].required = False  # Комментарий необязательный

    def clean_ad_receiver(self):
        receiver = self.cleaned_data.get("ad_receiver")
        print("Cleaning ad_receiver:", receiver)  # Отладочная информация
        if not receiver:
            raise ValidationError("Выберите объявление для обмена.")
            
        if not self.user or not self.ad_sender:
            raise ValidationError("Недостаточно данных для создания предложения.")
            
        # Проверяем, что выбранное объявление принадлежит пользователю
        if not self.own_ads.filter(pk=receiver.pk).exists():
            raise ValidationError(
                f"Выбранное объявление (ID: {receiver.pk}) недоступно для обмена. "
                f"Доступные ID: {list(self.own_ads.values_list('id', flat=True))}"
            )
            
        # Проверяем, что нельзя обменять на то же самое объявление
        if receiver.pk == self.ad_sender.pk:
            raise ValidationError("Нельзя предлагать обмен самому себе.")
            
        return receiver
