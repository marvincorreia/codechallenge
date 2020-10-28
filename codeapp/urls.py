from django.urls import path
from . import views

app_name = "codeapp"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("code/", views.CodeView.as_view(), name="code")
]
