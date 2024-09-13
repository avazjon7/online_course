from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from online_course.models import Course, Category, Video, Teacher,  Customer


class CategoryListView(ListView):
    model = Category
    template_name = 'online_course/index.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'online_course/course.html'
    context_object_name = 'category'

    def get_object(self):
        return get_object_or_404(Category, pk=self.kwargs['pk'])

class CourseListView(ListView):
    model = Course
    template_name ='online_course/course.html'
    context_object_name = 'online_course'
    ordering = ['name']
    success_url = reverse_lazy('courses_list')

class CourseDetailView(DetailView):
    model = Course
    template_name = 'online_course/course.html'
    context_object_name = 'course'

    def get_object(self):
        courses_id = self.kwargs.get('courses_id')
        return get_object_or_404(Course, id=courses_id)


class AboutView(TemplateView):
    template_name = 'online_course/about.html'

    def get_context_data(self, **kwargs):
        contex =super(AboutView,self).get_context_data(**kwargs)
        return contex

class TeacherListView(ListView):
    model = Teacher
    template_name = 'online_course/teacher.html'
    context_object_name = 'teachers'
    success_url = reverse_lazy('teachers_list')

class BlogListView(ListView):
    model = Blog
    template_name = 'online_course/blog.html'
    context_object_name = 'blogs'
    success_url = reverse_lazy('blogs_list')


class CustomerListView(ListView):
    model = Customer
    template_name = 'online_course/customer.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return super().get_queryset().order_by('-id')




