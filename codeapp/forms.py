from django import forms
from djangoeditorwidgets.widgets import MonacoEditorWidget

from . import models


class CodeModelForm(forms.ModelForm):
    class Meta:
        model = models.CodeModel
        fields = "__all__"
        widgets = {
            "code": MonacoEditorWidget(
                attrs={
                    "data-wordwrap": "on",
                    "data-language": "python",
                    'data-minimap': 'true'
                }
            )
        }
