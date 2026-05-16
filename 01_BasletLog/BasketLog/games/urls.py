from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
     # 例: 観戦記録の一覧画面（後ほどviewsに作る用として仮置き）
    # path('', views.diary_list, name='diary_list'),
    
    # 観戦記録の投稿画面 (URLは /games/create/ になります)
    path('create/', views.diary_create, name='diary_create'),
]
