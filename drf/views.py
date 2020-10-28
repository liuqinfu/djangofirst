from django.shortcuts import render

# Create your views here.

# 使用drf
from rest_framework.viewsets import ModelViewSet
from drf.models import Student
from drf.serialize import StudentSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
