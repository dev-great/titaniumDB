# serializers.py

from rest_framework import serializers
from .models import Review, Course,  Module, Video, Attachment, Assignment, AssignmentAnswer


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class AssignmentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentAnswer
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'user', 'course_title', 'detail', 'banner_image', 'modules', 'level',
                  'class_per_modules', 'is_document', 'is_ongoing', 'is_completed', 'created_on', 'updated_on']
        read_only_fields = ['user', 'created_on', 'updated_on']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'module', 'title', 'video_url', 'thumnail',
                  'is_ongoing', 'is_completed', 'duration', 'created_on', 'updated_on']
        read_only_fields = ['module', 'created_on', 'updated_on']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'module', 'title',
                  'document', 'created_on', 'updated_on']
        read_only_fields = ['module', 'created_on', 'updated_on']


class ModuleSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = Module
        fields = '__all__'
