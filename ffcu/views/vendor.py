from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordResetView
from coupons.forms import (UserAuthenticationForm,  AdminAuthenticationForm)
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from coupons.forms import CaptchaPasswordResetForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


class HomePageView(TemplateView):
    template_name = 'index.html'


def home(request):
    # return render(request, 'home.html',)
    #return HttpResponse("Test") #Exit Statement

    return redirect('vendor:dashboard')

# Redirect User from index to user portal by default
def index(request):
    return redirect('user_login')


class UserLoginView(LoginView):
    """
    Custom user login view.
    """
    form_class = UserAuthenticationForm
    template_name = 'registration/user_login.html'
    redirect_authenticated_user = True


class AdminLoginView(LoginView):
    """
    Custom admin login view.
    """
    form_class = AdminAuthenticationForm
    template_name = 'registration/admin_login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not form.get_user().user_type < 10:
            logout(self.request)
            return redirect('user_login')
        return super(AdminLoginView, self).form_valid(form)


class CaptchaPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class =  CaptchaPasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
