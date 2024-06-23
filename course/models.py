import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from authentication.models import CustomUser
from course.choices import CONTENT_TYPE, GRADE_TYPE, LEVEL_CHOICES

User = get_user_model()


def get_banner_image_upload_path(instance, filename):
    folder_path = f"class/course/{timezone.now().strftime('%Y/%m/%d')}/"
    return folder_path + filename


def get_video_banner_upload_path(instance, filename):
    folder_path = f"class/course/videos/banner/{instance.class_id}/{timezone.now().strftime('%Y/%m/%d')}/"
    return folder_path + filename


def get_attachment_upload_path(instance, filename):
    folder_path = f"class/course/videos/document/{instance.class_id}/{timezone.now().strftime('%Y/%m/%d')}/"
    return folder_path + filename


class Course(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=250)
    detail = models.TextField(db_index=True, null=True, blank=True)
    banner_image = models.ImageField(
        upload_to=get_banner_image_upload_path, null=False, blank=False)
    modules = models.IntegerField()
    level = models.CharField(
        max_length=30, choices=LEVEL_CHOICES, default='STANDARD')
    class_per_modules = models.IntegerField()
    is_document = models.BooleanField(default=True)
    is_ongoing = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.course_title)


class Module(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    detail = models.TextField(db_index=True, null=True, blank=True)
    thumnail = models.ImageField(
        upload_to=get_banner_image_upload_path, null=False, blank=False)
    is_assessment = models.BooleanField(default=True)
    is_ongoing = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)


class Video(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    video_url = models.TextField(db_index=True, null=False, blank=False)
    thumnail = models.ImageField(
        upload_to=get_attachment_upload_path, null=False, blank=False)
    is_ongoing = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    duration = models.DurationField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)


class Attachment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    document = models.FileField(
        upload_to=get_attachment_upload_path, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)


class Assignment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(db_index=True, null=False, blank=False)
    content_type = models.CharField(
        max_length=2, choices=CONTENT_TYPE, default='TI')
    text_answer = models.TextField(null=True, blank=True)
    file_answer = models.FileField(
        upload_to=get_attachment_upload_path, null=True, blank=True)
    grade = models.CharField(
        max_length=15, choices=GRADE_TYPE,  null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)


class AssignmentAnswer(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    text_answer = models.TextField(null=True, blank=True)
    file_answer = models.FileField(
        upload_to=get_attachment_upload_path, null=True, blank=True)
    grade = models.CharField(
        max_length=15, choices=GRADE_TYPE,  null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True, db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Review by {self.user.email}"
