from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.UserProfileUpdateView.as_view(), name="profile-update"),
    path(
        "password/change/", views.PasswordChangeView.as_view(), name="password-change"
    ),
]
