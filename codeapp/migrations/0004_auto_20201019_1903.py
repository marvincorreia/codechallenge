# Generated by Django 3.1.2 on 2020-10-19 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeapp', '0003_auto_20201019_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(choices=[('c', 'C'), ('cpp', 'C++'), ('python', 'Python'), ('java', 'Java'), ('go', 'Go'), ('typescript', 'TypeScript')], max_length=20),
        ),
    ]
