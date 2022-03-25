from django.db import router
from django.urls import path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(prefix = 'courses', viewset= views.CourseViewsets, basename= 'course')
routers.register(prefix = 'lessons', viewset=views.LessonViewsets, basename = 'lesson')
routers.register(prefix = 'categories',viewset= views.CategoryViewsets, basename= 'category')
routers.register(prefix = 'comments', viewset=views.CommentViewSet, basename='comment')
routers.register(prefix = 'users', viewset=views.UserViewSet, basename='user')
urlpatterns = [
    path('', include(routers.urls)),
]