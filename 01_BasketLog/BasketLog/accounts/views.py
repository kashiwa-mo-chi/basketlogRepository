from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from games.models import Diary
from django.contrib.auth.decorators import login_required
from spots.models import ArenaFacility, ArenaNearbySpot
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import RegistForm, EmailChangeForm, UsernameChangeForm





class HomeView(TemplateView):
    template_name = 'accounts/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_diaries'] = Diary.objects.filter(status=1).order_by('-watch_date')[:2]

        return context

class RegistUserView(CreateView):
    template_name = 'accounts/regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:user_login')

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:user_login')

@login_required
def mypage(request):
    return render(request, "accounts/mypage.html")

@login_required
def history(request):
    tab = request.GET.get("tab", "facility")

    facility_posts = ArenaFacility.objects.filter(
        user=request.user        
    ).order_by("-created_at")

    nearby_posts = ArenaNearbySpot.objects.filter(
        user=request.user        
    ).order_by("-created_at")

    context = {
        "tab": tab,
        "facility_posts": facility_posts,
        "nearby_posts": nearby_posts,
    }

    return render(request, "accounts/history.html", context)

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:mypage")
    success_message = "パスワードを変更しました"

class EmailChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EmailChangeForm
    template_name = "accounts/email_change.html"
    success_url = reverse_lazy("accounts:mypage")
    success_message = "メールアドレスを変更しました"

    def get_object(self):
        return self.request.user
    
class UsernameChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UsernameChangeForm
    template_name = "accounts/username_change.html"
    success_url = reverse_lazy("accounts:mypage")
    success_message = "ユーザ名を変更しました"

    def get_object(self):
        return self.request.user