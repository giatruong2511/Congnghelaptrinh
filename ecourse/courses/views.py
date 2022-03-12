from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .models import Course
from .serializers import CourseSerializer


class CourseViewsets(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active = True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
