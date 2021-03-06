from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from .models import  Category, Course, Lesson, Tag, User , Comment, Action, Rating
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'

class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    form = LessonForm
    inlines = [LessonTagInlineAdmin, ]


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'

class CourseAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'category']
    readonly_fields = ['image_view']

    def image_view(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=course.image.name)
            )

    inlines = [LessonInlineAdmin, ]

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name', 'created_date']
    list_display = ['id', 'name', 'created_date']

class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()
        stats = Course.objects \
                .annotate(lesson_count=Count('my_lession')) \
                .values('id', 'subject', 'lesson_count')

        return TemplateResponse(request,'admin/course-stats.html', {
            'course_count': count,
            'course_stats': stats
        })

admin_site = CourseAppAdminSite(name='myadmin')

admin_site.register(User)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag)
admin_site.register(Comment)
admin_site.register(Action)
admin_site.register(Rating)



