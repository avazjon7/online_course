import csv
import json
from datetime import datetime
from typing import io

import openpyxl
from django.forms import model_to_dict
from django.http import HttpResponse
from django.views.generic import View, TemplateView, DetailView
from django.views.generic import ListView

from django.shortcuts import render
from online_course.models import Course, Category, Teacher, Blog, Video


# Create your views here.


class HomeView(View):
    template_name = 'online_course/index.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        courses = Course.objects.all()
        teachers = Teacher.objects.all()
        context = {'categories': categories, 'courses': courses, 'teachers': teachers}
        return render(request, self.template_name, context)


class CategoryListView(View):
    model = Category
    context_object_name = 'categories'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'online_course/base/base.html', context)


class TeacherListView(ListView):
    model = Teacher
    context_object_name = 'teachers'
    template_name = 'online_course/teacher.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherListView, self).get_context_data(**kwargs)
        teachers = self.get_queryset()
        context['teachers'] = teachers

        return context


class CourseListview(View):
    template_name = 'online_course/course.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        courses = Course.objects.all()
        context = {'categories': categories, 'courses': courses}
        return render(request, self.template_name, context)


class CourseDetailView(DetailView):
    model = Video
    template_name = 'online_course/course_details.html'
    context_object_name = 'videos'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        videos = Video.objects.filter(course=course.id)
        context['videos'] = videos

        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = 'online_course/video-detail.html'
    context_object_name = 'video'


class AboutView(TemplateView):
    template_name = 'online_course/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        return context


class BlogListView(ListView):
    model = Blog
    template_name = 'online_course/blog.html'
    context_object_name = 'blogs'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all()
        teachers = Teacher.objects.all()
        video = Video.objects.all()
        context['courses'] = courses
        context['teachers'] = teachers
        context['video'] = video
        return context


class ExportDataView(View):
    """ This class is used to export data"""

    def get(self, request, *args, **kwargs):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        format = request.GET.get('format')

        if format == 'csv':
            return self.export_csv(date)

        elif format == 'json':
            return self.export_json(date)

        elif format == 'xlsx':
            return self.export_xlsx(date)

        else:
            return HttpResponse('Bad Request', status=400)

    def export_csv(self, date):
        meta = Video._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={Video._meta.object_name}-{date}.csv'

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in Video.objects.all():
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_json(self, date, CustomJSONEncoder=None):
        response = HttpResponse(content_type='application/json')
        customers = Video.objects.all()
        data = []

        for customer in customers:
            customer_dict = model_to_dict(customer)
            if 'image_field' in customer_dict:
                customer_dict['image_field'] = customer_dict['image_field'].url if customer_dict[
                    'image_field'] else None
            data.append(customer_dict)

        response.write(json.dumps(data, indent=4, cls=CustomJSONEncoder))
        response['Content-Disposition'] = f'attachment; filename=customers-{date}.json'

        return response

    def export_xlsx(self, date):
        customers = Video.objects.all()
        meta = Video._meta
        field_names = [field.name for field in meta.fields]
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Video"
        worksheet.append(field_names)
        for customer in customers:
            row = []
            for field in field_names:
                value = getattr(customer, field)
                if hasattr(value, 'url'):
                    value = value.url
                elif isinstance(value, datetime.datetime):
                    if value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, datetime.date):
                    value = value.strftime('%Y-%m-%d')
                row.append(value)
            worksheet.append(row)
        virtual_workbook = io.BytesIO()
        workbook.save(virtual_workbook)
        virtual_workbook.seek(0)
        response = HttpResponse(content=virtual_workbook.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=customers-{date}.xlsx'
        return response