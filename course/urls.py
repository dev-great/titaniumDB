from django.urls import path
from .views import (
    ReviewView,
    AssignmentListAPIView,
    AssignmentAnswerCreateAPIView,
    ReviewDetailView,
    AssignmentAPIView,
    CourseCreateView,
    ModuleCreateView,
    ModuleAPIView,
    AssignmentCreateAPIView,
    CourseAPIView,
    CourseListAPIView
)

urlpatterns = [
    path('reviews/', ReviewView.as_view(), name='review-list'),
    path('reviews/<uuid:id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('courses/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseAPIView.as_view(), name='course-detail'),
    path('courses/list/', CourseListAPIView.as_view(), name='course-list'),
    path('modules/', ModuleCreateView.as_view(), name='module-create'),
    path('modules/<int:pk>/', ModuleAPIView.as_view(), name='module-detail'),
    path('assignments/', AssignmentCreateAPIView.as_view(),
         name='assignment-create'),
    path('assignments/<int:pk>/', AssignmentAPIView.as_view(),
         name='assignment-detail'),
    path('assignments/module/<int:pk>/',
         AssignmentListAPIView.as_view(), name='assignment-list'),
    path('answers/', AssignmentAnswerCreateAPIView.as_view(),
         name='assignment-answer-create'),
]
