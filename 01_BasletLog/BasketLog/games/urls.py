from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
     #観戦記録の一覧画面
    path('diary/list/', views.diary_list, name='diary_list'),
    
    # 観戦記録の投稿画面 (URLは /games/create/ になります)
    path('create/', views.diary_create, name='diary_create'),

    path('diary/<int:diary_id>/', views.diary_detail, name='diary_detail'),
    path('diary/public/', views.public_diary_list, name='public_diary_list'),
]
