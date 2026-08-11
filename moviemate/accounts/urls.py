from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
     path("profile/", views.profile_view, name="profile"),
    path("profile/edit/",views.edit_profile,name="edit_profile"),
    path("profile/change-password/",views.change_password,name="change_password"),
    path("profile/delete/",views.delete_account,name="delete_account"),
]