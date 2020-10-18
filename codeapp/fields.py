# from django_monaco_editor.models import MonacoEditorModelField as mMonacoEditorModelField
# from django_monaco_editor.fields import MonacoEditorField
# from django_monaco_editor.widgets import MonacoEditorWidget
#
#
# class MonacoEditorModelField(mMonacoEditorModelField):
#     def formfield(self, **kwargs):
#         defaults = {
#             'form_class': MonacoEditorField,
#             'widget': MonacoEditorWidget
#         }
#         defaults.update(**kwargs)
#         return super(MonacoEditorModelField, self).formfield(**defaults)
