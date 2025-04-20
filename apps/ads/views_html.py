from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .forms import AdForm
from .forms import ProposalForm
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
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        if category:
            qs = qs.filter(category__icontains=category)
        if condition:
            qs = qs.filter(condition=condition)
        return qs


class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user != self.object.user:
            # Исключаем текущее объявление из списка
            context['user_ads'] = Ad.objects.filter(user=self.request.user).exclude(pk=self.object.pk)
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:ad_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:ad_list")

    def test_func(self):
        return self.get_object().user == self.request.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = "ads/confirm_delete.html"
    success_url = reverse_lazy("ads:ad_list")

    def test_func(self):
        return self.get_object().user == self.request.user


# --- Предложения обмена ------------------------------------------------------

class ProposalCreateView(LoginRequiredMixin, CreateView):
    form_class = ProposalForm
    success_url = reverse_lazy("ads:proposal_list")

    def get_ad(self):
        return get_object_or_404(Ad, pk=self.kwargs["ad_id"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        ad_sender = self.get_ad()
        kwargs["ad_sender"] = ad_sender
        kwargs["user"] = self.request.user  # Добавляем текущего пользователя
        print("Form kwargs:", kwargs)  # Отладочная информация
        print("Available ads for user:", Ad.objects.filter(user=self.request.user).values_list('id', flat=True))
        return kwargs

    def post(self, request, *args, **kwargs):
        print("POST data:", request.POST)  # Отладочная информация
        form = self.get_form()
        print("Form queryset:", form.fields['ad_receiver'].queryset.values_list('id', flat=True))  # Отладочная информация
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("Form errors:", form.errors)  # Отладочная информация
            return self.form_invalid(form)

    def form_valid(self, form):
        ad_sender = self.get_ad()
        form.instance.ad_sender = ad_sender
        try:
            self.object = form.save()
            messages.success(self.request, "Предложение отправлено.")
            return redirect("ads:proposal_list")
        except IntegrityError as e:
            print("IntegrityError:", str(e))  # Отладочная информация
            messages.error(self.request, "Вы уже отправляли такое предложение.")
            return redirect("ads:ad_detail", pk=ad_sender.pk)

    def form_invalid(self, form):
        ad_sender = self.get_ad()
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return redirect("ads:ad_detail", pk=ad_sender.pk)

    def get(self, request, *args, **kwargs):
        """При GET-запросе перенаправляем на страницу объявления"""
        ad = self.get_ad()
        return redirect("ads:ad_detail", pk=ad.pk)