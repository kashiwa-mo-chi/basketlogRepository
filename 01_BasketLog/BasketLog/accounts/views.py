from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import RegistForm
from games.models import Diary
from django.contrib.auth.decorators import login_required
from spots.models import ArenaFacility, ArenaNearbySpot



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

