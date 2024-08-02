# Generated by Django 5.0.6 on 2024-07-26 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="student_number",
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.CreateModel(
            name="CurrentCourseStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_carried", models.BooleanField(default=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.currentcourse",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.student",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="currentcourse",
            name="students",
            field=models.ManyToManyField(
                related_name="current_courses",
                through="students.CurrentCourseStatus",
                to="students.student",
            ),
        ),
        migrations.CreateModel(
            name="RepeatedCourseStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_carried", models.BooleanField(default=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.repeatedcourse",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.student",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="repeatedcourse",
            name="students",
            field=models.ManyToManyField(
                related_name="repeated_courses",
                through="students.RepeatedCourseStatus",
                to="students.student",
            ),
        ),
    ]