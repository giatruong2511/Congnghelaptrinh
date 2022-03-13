from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from .models import Course, Lesson, Category
from .serializers import CourseSerializer, LessonSerializer, CategorySerialzer


class CourseViewsets(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        courses = Course.objects.filter(active = True)

        q = self.request.query_params.get('q')
        if q is not None:
            courses =  Course.objects.filter(subject__icontains = q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            courses = courses.filter(category_id = cate_id)
        return courses

class CategoryViewsets(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer

class LessonViewsets(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active = True)
    serializer_class = LessonSerializer