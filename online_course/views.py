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


