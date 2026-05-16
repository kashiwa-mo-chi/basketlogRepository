from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import RegistForm

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class RegistUserView(CreateView):
    template_name = 'accounts/regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:user_login')

class UserLoginView(LoginView):
    template_name = 'accounts/user-login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:user_login')