from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from students.filters import CourseFilter
from students.models import Course, Student
from students.serializers import CourseSerializer, StudentSerializer


class CoursesViewSet(ModelViewSet, ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter

    def get(self, request, *args, **kwargs):
        sensor = Course.objects.all()
        ser = CourseSerializer(sensor, many=True)
        return Response(ser.data)


class StudentsViewSet(CreateAPIView, ModelViewSet, ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



