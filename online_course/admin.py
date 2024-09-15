from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe

from online_course.models import Course, Teacher, Category, Blog, Video, Comment


# Register your models here.

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id','name', 'category', 'price', 'teachers', 'preview_image')
    search_fields = ('name', 'category')
    list_filter = ('category',)

    def preview_image(self, obj):
        if obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 30px;">')

    preview_image.short_description = 'Image'


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id','full_name', 'preview_image')

    def preview_image(self, obj):
        if obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 30px;">')

    preview_image.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id','title', 'preview_image')

    def preview_image(self, obj):
        if obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 30px;">')

    preview_image.short_description = 'Image'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'category', 'image', 'description')  # Ensure 'description' is a valid field


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'file')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)
    context = 'video'


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at', 'video')
    ordering = ('-created_at',)