from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from . import forms
from django.urls import reverse_lazy
from . import models


# Create your views here.

def home_redirect_view(request):
    return redirect('codeapp:home')


class Home(TemplateView):
    template_name = 'codeapp/home.html'


class CodeView(FormView):
    template_name = "codeapp/code.html"
    form_class = forms.CodeModelForm
    success_url = reverse_lazy("codeapp:code")

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if 'langs' not in kwargs:
            kwargs['langs'] = models.Language.get_active_langs()
        return super().get_context_data(**kwargs)


class TestView(TemplateView):
    template_name = "codeapp/test.html"
