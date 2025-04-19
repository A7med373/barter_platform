from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AdForm, ProposalForm
from .models import Ad


# --- Объявления --------------------------------------------------------------

class AdListView(ListView):
    model = Ad
    template_name = "ads/ad_list.html"
    paginate_by = 20
    context_object_name = "ads"

    def get_queryset(self):
        qs = Ad.objects.all().order_by("-created_at")
        q = self.request.GET.get("q")
        category = self.request.GET.get("category")
        condition = self.request.GET.get("condition")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category=category)
        if condition:
            qs = qs.filter(condition=condition)
        return qs


class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"
    success_url =  reverse_lazy("ads:ad_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"
    success_url =  reverse_lazy("ads:ad_list")

    def test_func(self):
        return self.get_object().user == self.request.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = "ads/confirm_delete.html"
    success_url =  reverse_lazy("ads:ad_list")

    def test_func(self):
        return self.get_object().user == self.request.user


# --- Предложения обмена ------------------------------------------------------

class ProposalCreateView(LoginRequiredMixin, CreateView):
    form_class = ProposalForm
    template_name = "ads/proposal_form.html"
    success_url =  reverse_lazy("ads:ad_list")

    def form_valid(self, form):
        form.instance.ad_sender_id = self.kwargs["ad_id"]
        return super().form_valid(form)
