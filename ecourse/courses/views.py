from django.shortcuts import render
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (Course, Lesson, Category,
                     Comment, Action, Rating, LessonView,
                     User
                     )
from .serializers import (CourseSerializer, LessonSerializer,
                        CategorySerialzer, LessonDetailSerializer,
                        CommentSerializer, CreateCommentSerializer,
                        ActionSerializer, RatingSerializer,
                        LessonViewSerializer, UserSerializer )
from .paginators import CoursePaginator
from django.db.models import F
from .perms import CommentOwnerPermisson

class CourseViewsets(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CoursePaginator

    def get_queryset(self):
        courses = Course.objects.filter(active = True)

        q = self.request.query_params.get('q')
        if q is not None:
            courses =  Course.objects.filter(subject__icontains = q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            courses = courses.filter(category_id = cate_id)
        return courses

    @swagger_auto_schema(
        operation_description='Get the lessons of a course',
        responses={
            status.HTTP_200_OK: LessonSerializer()
        }
    )
    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        # course = Course.objects.get(pk=pk)
        courses = self.get_object()
        lessons = courses.lessons.filter(active=True)

        kw = request.query_params.get('kw')
        if kw:
            lessons = lessons.filter(subject__icontains=kw)

        return Response(data=LessonSerializer(lessons, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class CategoryViewsets(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(name__icontains=kw)

        return query


class LessonViewsets(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active = True)
    serializer_class = LessonDetailSerializer


    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


    @swagger_auto_schema(
        operation_description='Get the comments of a lesson',
        responses={
            status.HTTP_200_OK: CommentSerializer()
        }
    )
    @action(methods=['post'], url_path='add-comment', detail=True)
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content = content,
                                       lesson = self.get_object(),
                                       user = request.user)
            return  Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        lesson = self.get_object()
        comments = lesson.comments.select_related('user').filter(active=True)
        kw = self.request.query_params.get('kw')
        if kw:
            comments = comments.filter(content__icontains=kw)
        return Response(CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = Action.objects.create(type = action_type, lesson = self.get_object(),
                                       creator = request.user)
            return Response(ActionSerializer(action).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='rating', detail=True)
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            rate = Rating.objects.create(rating=rating, lesson = self.get_object(),
                                       creator = request.user)
            return Response(RatingSerializer(rate).data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='views', detail=True)
    def inc_view(self, request, pk):
        v, created = LessonView.objects.get_or_create(lesson = self.get_object())
        v.views = F('views') + 1
        v.save()

        v.refresh_from_db()

        return Response(LessonViewSerializer(v).data, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPermisson()]

        return [permissions.IsAuthenticated()]

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserSerializer