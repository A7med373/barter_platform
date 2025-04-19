from django import forms
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