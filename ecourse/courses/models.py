from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/%Y/%m/',
                      null=True, blank=True)

class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(ModelBase):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name




class Course(ModelBase):
    subject = models.CharField(max_length=255, null=False)
    description = models.TextField(null= True, blank=True)
    image = models.ImageField(upload_to='courses/%Y/%m/',
                              null=True, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ('subject', 'category')

class Lesson(ModelBase):
    class Meta:
        unique_together = ('subject', 'course')

    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='lessons/%Y/%m/',
                              null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', related_query_name='my_lession' )
    tags = models.ManyToManyField('Tag', blank=True,
                                  related_name='lessons')
    def __str__(self):
        return self.subject

class Comment(ModelBase):
    content = models.TextField()
    lesson = models.ForeignKey(Lesson,
                               related_name='comments',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ActionBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Action(ActionBase):
    LIKE, HAHA, HEART, SAD = range(4)
    ACTIONS = [
        (LIKE, 'like'),
        (HAHA, 'haha'),
        (HEART, 'heart'),
        (SAD, 'sad')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)

class Rating(ActionBase):
    rating = models.PositiveSmallIntegerField(default=0)


class LessonView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
