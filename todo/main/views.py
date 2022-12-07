from django.shortcuts import render, HttpResponse, redirect

from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator

from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode

from django.core.exceptions import ValidationError

from .models import *
from .forms import *
# Create your views here.

User = get_user_model()

class Home(LoginRequiredMixin, ListView):
    
    model = ToDoModels
    template_name = 'main/home.html'
    context_object_name = 'alltodo'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alltodo'] = context['alltodo'].filter(User=self.request.user)
        return context

class DetailTask(LoginRequiredMixin, DetailView):
    
    model = ToDoModels
    template_name = 'main/view.html'
    context_object_name = 'task'
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if self.model.objects.filter(Q(User=self.request.user) & Q(pk=pk)).exists():
            return super().get(request, *args, **kwargs)
        else:
            return redirect('home')
        
class CreateTask(LoginRequiredMixin, CreateView):
    
    model = ToDoModels
    template_name = 'main/create.html'
    context_object_name = 'create'
    fields = ['TaskTitle', 'TaskText', 'Complete']
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        
        form.instance.User = self.request.user
        return super(CreateTask, self).form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    
    model = ToDoModels
    template_name = 'main/create.html'
    context_object_name = 'update'
    fields = ['TaskTitle', 'TaskText', 'Complete']
    success_url = reverse_lazy('home')
    
class DeleteTask(LoginRequiredMixin, DeleteView):
    
    model = ToDoModels
    template_name = 'main/delete.html'
    context_object_name = 'delete'
    success_url = reverse_lazy('home')
    
class CustomLogin(LoginView):
    
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')

class UserRegister(CreateView):
    
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('home')

class ViewUserProfile(DetailView):
    
    model = CustomUser
    template_name = 'main/profile-view.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'UPobj'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_slug = self.kwargs.get(self.slug_url_kwarg)
        TasksCount = self.model.objects.get(username=get_slug).users.count()
        context['amount'] = TasksCount
        context['is_true'] = get_slug == self.request.user.username
        return context

class EditeUserProfile(UpdateView):
    
    form_class = UpdateUserProfile
    model = CustomUser
    template_name = 'main/profile-edite.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        get_user = self.kwargs.get(self.slug_url_kwarg)
        if get_user == self.request.user.username:
            return super().get(request, *args, **kwargs)
        return redirect('home')
