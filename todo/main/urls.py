from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from .views import (CreateTask, CustomLogin,
                    DeleteTask, DetailTask,
                    EditeUserProfile, EmailVerify,
                    Home, LogoutView,
                    UpdateTask, UserRegister,
                    ViewUserProfile)


urlpatterns = [path('', view=Home.as_view(), name='home'),
     path('login/', view=CustomLogin.as_view(), name='login'),
     path('logout/', view=LogoutView.as_view(next_page='login'), name='logout'),
     path('task/<int:pk>', view=DetailTask.as_view(), name='viewtask'),
     path('create-task', view=CreateTask.as_view(), name='createTask'),
     path('update-task/<int:pk>', view=UpdateTask.as_view(), name='updateTask'),
     path('delete-task/<int:pk>', view=DeleteTask.as_view(), name='deleteTask'),
     path('register', view=UserRegister.as_view(), name='registration'),
     path('profile/view/<str:username>', view=ViewUserProfile.as_view(), name='profile-view'),
     path('profile/edite/<str:username>', view=EditeUserProfile.as_view(), name='profile-edite'),
     path('reset-password/', view=auth_views.PasswordResetView.as_view(), name='reset_password'),

     path('reset-password-sent/', view=auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

     path('reset/<uidb64>/<token>', view=auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

     path('reset-password-complete', view=auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),

     path('verify_email/<uidb64>/<token>', view=EmailVerify.as_view(), name='verify_url'),

     path('confirm_email/',
         view=TemplateView.as_view(template_name='main/registration/confirm_email.html'),
         name='confirm_email')
]
