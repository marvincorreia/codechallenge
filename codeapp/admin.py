from django.contrib import admin
from django.db import models as djmodels
from . import models

from djangoeditorwidgets.widgets import MonacoEditorWidget


# Register your models here.

@admin.register(models.CodeModel)
class CodeModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        djmodels.TextField: {'widget': MonacoEditorWidget(
            attrs={'data-minimap': 'true', "data-wordwrap": "on", "data-language": "python"}
        )}
    }


@admin.register(models.Language)
class LanguageModelAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Language._meta.fields if f.name != 'id']
