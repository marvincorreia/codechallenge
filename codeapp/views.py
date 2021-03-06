from django.shortcuts import render, redirect
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import FormView, TemplateView
from . import forms
from django.urls import reverse_lazy
from . import models
from django.http import Http404
from django.conf import settings


# Create your views here.

def home_redirect_view(request):
    return redirect('codeapp:home')


class BaseView(TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        if 'langs' not in kwargs:
            kwargs['langs'] = models.Language.get_active_langs()
        if 'static_url' not in kwargs:
            kwargs['static_url'] = settings.STATIC_URL
        return super(BaseView, self).get_context_data(**kwargs)


class Home(BaseView):
    template_name = 'codeapp/home.html'


class CodeView(BaseView, FormView):
    template_name = "codeapp/code.html"
    form_class = forms.CodeModelForm
    success_url = reverse_lazy("codeapp:code")

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(CodeView, self).get_context_data(**kwargs)


class DocDetailView(BaseView, FormView):
    template_name = "codeapp/docs/"
    form_class = forms.CodeModelForm

    def get(self, request, *args, **kwargs):
        return super(DocDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(DocDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.template_name += kwargs["lang"] + ".html"
            get_template(self.template_name)
            return super(DocDetailView, self).dispatch(request, *args, **kwargs)
        except TemplateDoesNotExist:
            raise Http404
