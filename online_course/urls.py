from django.urls import path
from online_course import views
from online_course import auth
from online_course.auth import ActivateAccountView

urlpatterns = [
    path('index', views.CategoryListView.as_view(), name='index'),
    path('courses_list',views.CourseListView.as_view(), name='courses_list'),
    path('about', views.AboutView.as_view(), name='about'),
    path('teachers',views.TeacherListView.as_view(), name='teachers_list'),
    path('blog_list',views.BlogListView.as_view(), name='blog_list'),


    #auth
    path('login-page/', auth.LoginPage.as_view(), name='login_page'),
    path('register-page/', auth.RegisterPage.as_view(), name='register_page'),
    path('logout_page/', auth.logout_page, name='logout_page'),
    path('send-email/', auth.SendingEmail.as_view(), name = 'sending_email'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

]