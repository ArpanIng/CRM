from django.contrib.auth import views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm


class LoginView(views.LoginView):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        """Block authenticated user from accessing login URL"""
        if self.request.user.is_authenticated:
            return redirect("homepage")
        return super().dispatch(request, *args, **kwargs)


class LogoutView(views.LogoutView):
    template_name = "accounts/logout.html"


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

    def dispatch(self, request, *args, **kwargs):
        """Block authenticated user from accessing signup URL"""
        if self.request.user.is_authenticated:
            return redirect("homepage")
        return super().dispatch(request, *args, **kwargs)


class PasswordResetView(views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    template_name = "accounts/password_reset_form.html"


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
