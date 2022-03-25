from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Course, Lesson, Tag, Category, User, Comment, Action, Rating, LessonView

class CourseSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, obj):
        request = self.context['request']
        name = obj.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = Course
        fields = ['id', 'subject','image', 'created_date', 'category']


class CategorySerialzer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'course_id', 'created_date', 'tags']

    def get_image(self, obj):
        request = self.context['request']
        name = obj.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)


class LessonDetailSerializer(LessonSerializer):
    class Meta:
        model = Lesson
        fields = LessonSerializer.Meta.fields + ['content']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'lesson']



class CommentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        exclude = ['active']

class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'type', 'created_date']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'created_date']


class LessonViewSerializer(ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['id', 'views', 'lesson']