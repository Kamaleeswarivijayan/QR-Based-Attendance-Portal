from django.urls import path
from .views import admin_dashboard
from .views import admin_dashboard, admin_profile
import dashboard.views as views
urlpatterns = [
    path("", admin_dashboard, name="admin_dashboard"),
    path("profile/", admin_profile, name="admin_profile"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]