# Generated by Django 5.0.6 on 2024-06-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0004_student_year_alter_student_field_of_study"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="year",
        ),
        migrations.AlterField(
            model_name="student",
            name="field_of_study",
            field=models.CharField(max_length=50),
        ),
    ]
