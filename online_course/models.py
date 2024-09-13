from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)


class Teacher(models.Model):ini
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telegram_url = models.URLField(max_length=500)
    instagram_url = models.URLField(max_length=500)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField(default=0)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Customer(models.Model):
    phone_number = models.CharField(max_length=11)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)




class Video(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    file = models.FileField(upload_to='videos/')
    course_id = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    id = models.AutoField(primary_key=True)
    message = models.TextField(max_length=500)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

