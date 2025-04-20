from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import SignUpForm


class SignUpView(CreateView):
    """
    Простая регистрация нового пользователя.
    После успешной регистрации редиректит на страницу логина.
    """
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Профиль пользователя.
    """
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class LogoutView(DjangoLogoutView):
    """
    Выход из системы.
    """
    next_page = "login"