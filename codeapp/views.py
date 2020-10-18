from django.shortcuts import render
from django.views.generic import FormView
from . import forms
from django.urls import reverse_lazy


# Create your views here.


class EditorTestView(FormView):
    template_name = "codeapp/index.html"
    form_class = forms.CodeModelForm
    success_url = reverse_lazy("codeapp:code")
