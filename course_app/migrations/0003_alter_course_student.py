# Generated by Django 3.2.5 on 2023-12-26 18:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_app', '0002_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(blank=True, null=True, related_name='student_courses', to=settings.AUTH_USER_MODEL, verbose_name='دانشجو'),
        ),
    ]
