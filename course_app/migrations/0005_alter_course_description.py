# Generated by Django 4.2 on 2024-02-26 05:55

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0004_alter_course_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=djrichtextfield.models.RichTextField(),
        ),
    ]