from django.contrib import admin

from django.urls import path

from users.views import LogoutPage
from users import views

urlpatterns = [

    path('logout/', LogoutPage.as_view(), name='logout'),
    path('login/', views.LoginPage.as_view(), name='login_page'),
    path('register/', views.RegisterPage.as_view(), name='register_page'),
    path('send-email/', views.SendingEmail.as_view(), name='sending_email'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    # path('courses/', CourseListView.as_view(), name='courses_list'),
]