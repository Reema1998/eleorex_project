"""ffcu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path, include
from ffcu.views import vendor, messages
from coupons.forms import AdminAuthenticationForm, PasswordChangeForm
# from django.contrib.messages import constants as messages
from django.conf.urls import handler404, handler500
from django.contrib.auth import views as coreViews
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
# from .views import vendor
from coupons import views

urlpatterns = [
    path('home/', vendor.home, name='home'),
    # path('', vendor.home, name="index"),

    path('', vendor.index, name="index"),
    path('user/', vendor.UserLoginView.as_view(), name='user_login'),
    path('password_reset/', vendor.CaptchaPasswordResetView.as_view(), name='password_reset'),
    path('admin/', vendor.AdminLoginView.as_view(), name='login'),

    path('logout/', coreViews.LogoutView.as_view(), name='logout'),
    path('', include('coupons.urls')),

# ]
] + [
    path('password_change/', coreViews.PasswordChangeView.as_view(
        success_url=reverse_lazy('login'),
        form_class=PasswordChangeForm),
        name='password_change'),
    path('password_change/done/', coreViews.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # # Work pending : Forgot Password flow
    # path('password_reset/', interview.CaptchaPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# #
#


handler404 = messages.error_404
handler500 = messages.error_500
