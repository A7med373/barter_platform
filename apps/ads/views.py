from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView

from .forms import ProposalForm
from .models import ExchangeProposal, Ad
from .views_html import ProposalCreateView


class ProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = "ads/proposal_list.html"
    context_object_name = "proposals"
    paginate_by = 20

    def get_queryset(self):
        qs = ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |
            Q(ad_receiver__user=self.request.user)
        ).select_related('ad_sender', 'ad_receiver', 'ad_sender__user', 'ad_receiver__user')

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)

        # Filter by type (sent/received)
        filter_type = self.request.GET.get('type')
        if filter_type == 'sent':
            qs = qs.filter(ad_sender__user=self.request.user)
        elif filter_type == 'received':
            qs = qs.filter(ad_receiver__user=self.request.user)

        return qs.order_by('-created_at')


class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = ExchangeProposal
    template_name = "ads/proposal_detail.html"
    context_object_name = "object"

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |
            Q(ad_receiver__user=self.request.user)
        ).select_related('ad_sender', 'ad_receiver')


class ProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = "ads/proposal_update.html"
    success_url = reverse_lazy('ads:proposal_list')

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_receiver__user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        status_display = form.instance.get_status_display()
        messages.success(self.request, f"Статус предложения изменен на '{status_display}'")
        return response

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.ad_receiver.user != self.request.user:
            raise PermissionDenied("Вы не можете изменять это предложение")
        return obj
