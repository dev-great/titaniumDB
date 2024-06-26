# Generated by Django 5.0.6 on 2024-06-11 07:48

import course.models
import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("course_title", models.CharField(max_length=250)),
                ("detail", models.TextField(blank=True, db_index=True, null=True)),
                (
                    "banner_image",
                    models.ImageField(
                        upload_to=course.models.get_banner_image_upload_path
                    ),
                ),
                ("modules", models.IntegerField()),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("BASIC", "Basic"),
                            ("STANDARD", "Standard"),
                            ("ADVANCE", "Advance"),
                        ],
                        default="STANDARD",
                        max_length=30,
                    ),
                ),
                ("class_per_modules", models.IntegerField()),
                ("is_document", models.BooleanField(default=True)),
                ("is_ongoing", models.BooleanField(default=False)),
                ("is_completed", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                ("detail", models.TextField(blank=True, db_index=True, null=True)),
                (
                    "thumnail",
                    models.ImageField(
                        upload_to=course.models.get_banner_image_upload_path
                    ),
                ),
                ("is_assessment", models.BooleanField(default=True)),
                ("is_ongoing", models.BooleanField(default=False)),
                ("is_completed", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.course"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=course.models.get_attachment_upload_path,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.module"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                ("description", models.TextField(db_index=True)),
                (
                    "content_type",
                    models.CharField(
                        choices=[
                            ("TO", "Text Only"),
                            ("IO", "Image Only"),
                            ("TI", "Text and Image"),
                        ],
                        default="TI",
                        max_length=2,
                    ),
                ),
                ("text_answer", models.TextField(blank=True, null=True)),
                (
                    "file_answer",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=course.models.get_attachment_upload_path,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.module"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("review", models.TextField(db_index=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.module"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                ("video_url", models.TextField(db_index=True)),
                (
                    "thumnail",
                    models.ImageField(
                        upload_to=course.models.get_attachment_upload_path
                    ),
                ),
                ("is_ongoing", models.BooleanField(default=False)),
                ("is_completed", models.BooleanField(default=False)),
                ("duration", models.DurationField(blank=True, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.module"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
    ]
