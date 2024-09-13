from django.contrib.auth.models import User
from django.db import models

from users.models import Users


# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telegram_url = models.URLField(max_length=500)
    instagram_url = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField(default=0)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Customer(models.Model):
    phone_number = models.CharField(max_length=11)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    file = models.FileField(upload_to='videos/')
    course_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Comment(models.Model):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0, 'No Rating'
        ONE = 1, '1 Star'
        TWO = 2, '2 Stars'
        THREE = 3, '3 Stars'
        FOUR = 4, '4 Stars'
        FIVE = 5, '5 Stars'

    id = models.AutoField(primary_key=True)
    message = models.TextField(max_length=500)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='comments')
    rating = models.PositiveSmallIntegerField(
        choices=RatingChoices.choices,
        default=RatingChoices.ZERO,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.video} (Rating: {self.rating})"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title