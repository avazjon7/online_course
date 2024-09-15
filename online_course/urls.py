from django.contrib import admin
from django.contrib.auth.context_processors import auth
from django.urls import path
from online_course import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('online_course/', views.CourseListview.as_view(), name='online_course'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('blog_list/', views.BlogListView.as_view(), name='blog_list'),
    path('detail/<int:pk>/', views.CourseDetailView.as_view(), name ='detail'),
    path('video-detail/<int:pk>/', views.VideoDetailView.as_view(), name='video'),
    # path('login-page/', auth.LoginPage.as_view(), name='login_page'),
    # path('register-page/', auth.RegisterPage.as_view(), name='register_page'),
    # path('logout_page/', auth.logout_page, name='logout_page'),

]


