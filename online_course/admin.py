from django.contrib import admin
from django.contrib.auth.models import User
from online_course.models import Category, Course,Teacher,Video,Customer,Comment

# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Video)
admin.site.register(Customer)
admin.site.register(Comment)

