import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from online_course.models import Course, Video, Customer, Blog, Comment
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from users.models import User
from datetime import datetime

def save_deleted_data(instance, file_dir, data):
    date = datetime.now().strftime("%Y,%b")
    file_path = os.path.join(BASE_DIR, file_dir, f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)


def send_notification_email(subject, message):
    from_email = EMAIL_DEFAULT_SENDER
    recipient_list = [user.email for user in User.objects.all()]
    send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Course)
def notify_course_created(sender, instance, created, **kwargs):
    if created:
        subject = 'Course added'
        message = f'{instance.title} added a new course.'
        send_notification_email(subject, message)


@receiver(pre_delete, sender=Course)
def save_deleted_course(sender, instance, **kwargs):
    course_data = {
        'id': instance.id,
        'title': instance.title,
        'description': instance.description,
        'image': str(instance.image),
        'price': instance.price,
        'category_id': instance.category_id,
        'teacher_id': instance.teacher_id,
        'slug': instance.slug,
    }
    save_deleted_data(instance, 'course/deleted_data/deleted_course', course_data)


@receiver(post_save, sender=Video)
def notify_video_created(sender, instance, created, **kwargs):
    if created:
        subject = 'Video added'
        message = f'{instance.title} added a new video.'
        send_notification_email(subject, message)


@receiver(pre_delete, sender=Video)
def save_deleted_video(sender, instance, **kwargs):
    video_data = {
        'id': instance.id,
        'title': instance.title,
        'duration': instance.duration,
        'file': str(instance.file),
        'course_id': instance.course_id,
    }
    save_deleted_data(instance, 'course/deleted_data/deleted_videos', video_data)


@receiver(post_save, sender=Comment)
def notify_comment_created(sender, instance, created, **kwargs):
    if created:
        subject = 'Comment added'
        message = f'New comment: {instance.content}'
        send_notification_email(subject, message)


@receiver(pre_delete, sender=Comment)
def save_deleted_comment(sender, instance, **kwargs):
    comment_data = {
        'id': instance.id,
        'rating': instance.rating,
        'content': instance.content,
        'user_id': instance.user_id,
        'video_id': instance.video_id,
    }
    save_deleted_data(instance, 'course/deleted_data/deleted_comments', comment_data)


@receiver(post_save, sender=Customer)
def notify_customer_created(sender, instance, created, **kwargs):
    if created:
        subject = 'Customer bought a course'
        message = f"Customer's number : {instance.phone} bought a new course."
        send_notification_email(subject, message)


@receiver(pre_delete, sender=Customer)
def save_deleted_customer(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'phone': instance.phone,
        'user_id': instance.user_id,
        'course_id': instance.course_id,
    }
    save_deleted_data(instance, 'course/deleted_data/deleted_customers', customer_data)


@receiver(post_save, sender=Blog)
def notify_blog_created(sender, instance, created, **kwargs):
    if created:
        subject = 'Blog created'
        message = f"Blog's title : {instance.title} created a new blog."
        send_notification_email(subject, message)


@receiver(pre_delete, sender=Blog)
def save_deleted_blog(sender, instance, **kwargs):
    blog_data = {
        'id': instance.id,
        'title': instance.title,
        'content': instance.body,
        'image': str(instance.image.url),
        'category_id': instance.category_id,
    }
    save_deleted_data(instance, 'course/deleted_data/deleted_blogs', blog_data)
