from django.urls import include, path
from django.contrib import admin
from ffcu.views import vendor
from coupons import views

# from .views import interview, interviewee, interviewer
from .views import *


urlpatterns = [
    # path('viddi_manager/', admin.site.urls),
    path('home/', vendor.home, name='home'),

    path('vendor/', include(([
        path('', views.manage_dashboard, name='dashboard'),

        path('vendors/', views.UserManagementListView.as_view(),
              name='user_management_list'),
        path('vendors/add/', views.InterviewerSignUpView.as_view(),
              name='user_management_add'),
        path('vendors/<int:pk>/', views.InterviewerUpdateView.as_view(),
              name='user_management_edit'),
        path('vendors/<int:pk>/delete/', views.InterviewerDeleteView.as_view(),
              name='user_management_delete'),

    ], 'vendor'), namespace='vendor')),
]
