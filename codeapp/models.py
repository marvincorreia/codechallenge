from django.db import models

LANGUAGES = (
    ('c', 'C'),
    ('cpp', 'C++'),
    ('python', 'Python'),
    ('java', 'Java'),
    ('go', 'Go'),
    ('typescript', 'TypeScript'),
    ('javascript', 'JavaScript'),
)


# Create your models here.

class CodeModel(models.Model):
    code = models.TextField(null=True, blank=True)


class Language(models.Model):
    name = models.CharField(max_length=20, unique=True, choices=LANGUAGES)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.get_name_display()

    @staticmethod
    def get_active_langs() -> list:
        """:return: List of active key/value wrapped Language
           like [{'value': 'python','display':'Python'},{...}]
        """
        return [dict(value=x.name, display=x.get_name_display()) for x in Language.objects.order_by('name').filter(active=True)]
