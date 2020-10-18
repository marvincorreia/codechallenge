from django.urls import path
from . import views

app_name = "codeapp"

urlpatterns = [
    path("", views.EditorTestView.as_view(), name="code")
]
