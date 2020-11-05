from django.urls import path
from . import views

app_name = "codeapp"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("code/", views.CodeView.as_view(), name="code"),
    path("docs/", views.BaseView.as_view(template_name='codeapp/docs/docs.html'), name="docs-list"),
    path("docs/<str:lang>", views.DocDetailView.as_view(), name="docs-detail")
]
