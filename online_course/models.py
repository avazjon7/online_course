from datetime import timedelta

from social_core.utils import slugify

from users.models import User
from django.db import models


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/categories/')

    def __str__(self):
        return self.title


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/teachers/', null=True, blank=True)
    telegram_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.full_name



    def __str__(self):
        return f'{self.phone} , {self.course_id}'

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    teachers = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    @property
    def joined(self):
        return f'{self.created_at.day} {self.created_at.month} {self.created_at.year}'

    @property
    def student_count(self):
        return self.customer.aggregate(student_count=models.Count('id'))['student_count'] or 0

    @property
    def comment_count(self):
        return self.videos.aggregate(comment_count=models.Count('comments__id'))['comment_count'] or 0

    @property
    def average_rating(self):
        return self.videos.aggregate(
            average_rating=models.Avg('comments__rating'))['average_rating'] or 0

    @property
    def total_duration(self):
        total_duration = sum((video.duration for video in self.videos.all()), timedelta())

        total_seconds = int(total_duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f'{hours}h {minutes}m {seconds}s'

class Customer(BaseModel):
    phone = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customer', null=True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='customer', null=True)

class Video(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    duration = models.DurationField(null=True, blank=True)
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    context = 'video'


    def __str__(self):
        return self.title


class Comment(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    text = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE, default=1, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    image = models.ImageField(upload_to='images/blogs/')
    description = models.TextField()
    created_at = models.DateTimeField()
