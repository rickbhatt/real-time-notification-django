from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.handle_login, name="login"),
    path(
        "check-loggedin-status/",
        views.check_logged_in_status,
        name="check-loggedin-status",
    ),
    path("logout/", views.handle_logout, name="logout"),
]
