from django.urls import path

from . import views

# Describes all app url endpoints
urlpatterns = [
    path("", views.index, name="index"),
    path("select-password", views.password_select, name="select-password"),
    path("create-account", views.create_account, name="create-account"),
    path("post", views.post, name="post"),
    path("logout", views.logout, name="logout"),
]