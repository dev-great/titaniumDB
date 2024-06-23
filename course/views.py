import logging
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from exceptions.custom_apiexception_class import CustomAPIException
from utils import custom_response
from .models import AssignmentAnswer, Course, Review, Module, Video, Assignment, Attachment
from .serializers import AssignmentAnswerSerializer, AssignmentSerializer, AttachmentSerializer, CourseSerializer, ModuleSerializer, ReviewSerializer, VideoSerializer
from rest_framework.response import Response
logger = logging.getLogger(__name__)


class ReviewView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            reviews = Review.objects.all()
            serializer = ReviewSerializer(reviews, many=True)
            return custom_response(status_code=status.HTTP_200_OK, message="Success", data=serializer.data)
        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

    @swagger_auto_schema(request_body=ReviewSerializer)
    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                review = serializer.save(user=request.user)
                return custom_response(status_code=status.HTTP_201_CREATED, message="Review created successfully", data=ReviewSerializer(review).data)
            except Exception as e:
                raise CustomAPIException(detail=str(
                    e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        else:
            return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)


class ReviewDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        try:
            review = Review.objects.get(id=id)
            serializer = ReviewSerializer(review)
            return custom_response(status_code=status.HTTP_200_OK, message="Success", data=serializer.data)
        except Review.DoesNotExist:
            raise CustomAPIException(
                detail="Review not found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class CourseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            try:
                course = serializer.save(user=request.user)
                return custom_response(status_code=status.HTTP_201_CREATED, message="Course created successfully", data=CourseSerializer(course).data)
            except Exception as e:
                raise CustomAPIException(detail=str(
                    e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        else:
            return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)


class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            error_msg = f"Course with id {pk} not found."
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the course: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        try:
            modules = Module.objects.filter(course=course)
            course_data = CourseSerializer(course).data
            modules_data = ModuleSerializer(modules, many=True).data
        except Exception as e:
            error_msg = f"An error occurred while retrieving the modules: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        response_data = {
            'course': course_data,
            'modules': modules_data
        }

        return custom_response(status_code=status.HTTP_200_OK, message="Course and modules fetched successfully", data=response_data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def patch(self, request, pk, format=None):
        try:
            course = Course.objects.get(id=pk, user=request.user)
        except Course.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Course not found or you do not have permission to edit this course")
        try:
            serializer = CourseSerializer(
                course, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Course updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            course = Course.objects.get(id=pk, user=request.user)
            course.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Course deleted successfully")

        except Course.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Course not found or you do not have permission to delete this course")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class CourseListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            level = request.query_params.get('level', None)
            detail = request.query_params.get('detail', None)
            course_title = request.query_params.get('course_title', None)

            filters = Q()
            if level:
                filters &= Q(level=level)
            if detail:
                filters &= Q(detail__icontains=detail)
            if course_title:
                filters &= Q(course_title__icontains=course_title)

            courses = Course.objects.filter(filters)
            if not courses.exists():
                raise CustomAPIException(
                    detail="No courses found", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

            serializer = CourseSerializer(courses, many=True)
            return custom_response(status_code=status.HTTP_200_OK, message="Courses retrieved successfully", data=serializer.data)

        except CustomAPIException as e:
            return custom_response(status_code=e.status_code, message=e.detail)
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class ModuleCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ModuleSerializer(many=True),
        responses={status.HTTP_201_CREATED: ModuleSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        module_data_list = request.data
        created_modules = []

        try:
            for module_data in module_data_list:
                serializer = ModuleSerializer(data=module_data)
                if serializer.is_valid():
                    # Create the Module instance
                    module = Module.objects.create(**serializer.validated_data)
                    created_modules.append(module)

                    # Create Video instances
                    videos_data = module_data.get('videos', [])
                    for video_data in videos_data:
                        Video.objects.create(module=module, **video_data)

                    # Create Attachment instances
                    attachments_data = module_data.get('attachments', [])
                    for attachment_data in attachments_data:
                        Attachment.objects.create(
                            module=module, **attachment_data)
                else:
                    raise CustomAPIException(detail=str(
                        serializer.errors), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

            # Serialize the created modules and return the response
            response_data = ModuleSerializer(created_modules, many=True).data
            return custom_response(
                status_code=status.HTTP_201_CREATED,
                message="Modules created successfully",
                data=response_data
            )
        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class ModuleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ModuleSerializer)
    def patch(self, request, pk, format=None):
        try:
            module = Module.objects.get(id=pk)
        except Module.DoesNotExist:
            error_msg = f"Module with id {pk} not found."
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the module: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        try:
            serializer = ModuleSerializer(
                module, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Module updated successfully", data=serializer.data)
            else:
                error_msg = f"Invalid data provided: {serializer.errors}"
                logger.error(error_msg)
                return CustomAPIException(detail=error_msg, status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while updating the module: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    @swagger_auto_schema(responses={200: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            module = Module.objects.get(id=pk)
        except Module.DoesNotExist:
            error_msg = f"Module with id {pk} not found."
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the module: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        try:
            module.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Module deleted successfully")
        except Exception as e:
            error_msg = f"An error occurred while deleting the module: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    def get(self, request, pk, format=None):
        try:
            module = Module.objects.get(id=pk)
        except Module.DoesNotExist:
            error_msg = f"Module with id {pk} not found."
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the module: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        try:
            videos = Video.objects.filter(module=module)
            attachments = Attachment.objects.filter(module=module)
            assignments = Assignment.objects.filter(module=module)

            module_data = ModuleSerializer(module).data
            videos_data = VideoSerializer(videos, many=True).data
            attachments_data = AttachmentSerializer(
                attachments, many=True).data
            assignments_data = AssignmentSerializer(
                assignments, many=True).data
        except Exception as e:
            error_msg = f"An error occurred while retrieving the related data: {str(e)}"
            logger.error(error_msg)
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        response_data = {
            'module': module_data,
            'videos': videos_data,
            'attachments': attachments_data,
            'assignments': assignments_data
        }

        return custom_response(status_code=status.HTTP_200_OK, message="Module and related data fetched successfully", data=response_data)


class AssignmentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AssignmentSerializer)
    def post(self, request, format=None):
        try:
            serializer = AssignmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_201_CREATED, message="Assignment created successfully", data=serializer.data)
            else:
                raise CustomAPIException(
                    detail=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class AssignmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            assignment = Assignment.objects.get(pk=pk)
            serializer = AssignmentSerializer(assignment)
            user = request.user
            assignment_answer = AssignmentAnswer.objects.filter(
                assignment=assignment, user=user).first()
            if assignment_answer:
                answer_serializer = AssignmentAnswerSerializer(
                    assignment_answer)
                response_data = {
                    'assignment': serializer.data,
                    'assignment_answer': answer_serializer.data
                }
            else:
                response_data = {
                    'assignment': serializer.data,
                    'assignment_answer': None
                }
            return custom_response(status_code=status.HTTP_200_OK, message="Assignment details retrieved", data=response_data)
        except Assignment.DoesNotExist:
            raise CustomAPIException(
                detail="Assignment not found", status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    @swagger_auto_schema(request_body=AssignmentSerializer)
    def patch(self, request, pk, format=None):
        try:
            assignment = Assignment.objects.get(pk=pk)
            serializer = AssignmentSerializer(
                assignment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Assignment updated successfully", data=serializer.data)
            else:
                raise CustomAPIException(
                    detail=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        except Assignment.DoesNotExist:
            raise CustomAPIException(
                detail="Assignment not found", status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            assignment = Assignment.objects.get(pk=pk)
            assignment.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Assignment deleted successfully")
        except Assignment.DoesNotExist:
            raise CustomAPIException(
                detail="Assignment not found", status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class AssignmentAnswerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AssignmentAnswerSerializer)
    def post(self, request, format=None):
        serializer = AssignmentAnswerSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            existing_answer = AssignmentAnswer.objects.filter(
                user=user, assignment=serializer.validated_data['assignment']
            ).first()
            if existing_answer:
                raise CustomAPIException(
                    detail="Assignment answer already exists for this user and assignment", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
            serializer.save(user=user)
            return custom_response(status_code=status.HTTP_201_CREATED, message="Assignment answer created successfully", data=serializer.data)
        else:
            return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)


class AssignmentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            assignments = Assignment.objects.filter(module_id=pk)
            if not assignments.exists():
                raise CustomAPIException(
                    detail="No assignments found for this module", status_code=status.HTTP_404_NOT_FOUND).get_full_details()
            serializer = AssignmentSerializer(assignments, many=True)
            return custom_response(status_code=status.HTTP_200_OK, message="Assignments retrieved successfully", data=serializer.data)
        except CustomAPIException as e:
            return custom_response(status_code=e.status_code, message=e.detail)
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))
