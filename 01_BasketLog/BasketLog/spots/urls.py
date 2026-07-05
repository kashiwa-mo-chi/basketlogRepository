from django.urls import path
from . import views

app_name = 'spots'

urlpatterns = [
    path('', views.arena_list, name='arena_list'),

    path('<int:arena_id>/', views.arena_top, name='arena_top'),

    path('<int:arena_id>/facility/new/', views.facility_post_create, name='facility_post_create'),
    path('<int:arena_id>/nearby/new/', views.nearby_post_create, name='nearby_post_create'),

    path('facility/<int:pk>/', views.facility_detail, name='facility_detail'),
    path('facility/<int:pk>/edit/', views.facility_post_update, name='facility_post_update'),
    path('facility/<int:pk>/delete/', views.facility_post_delete, name='facility_post_delete'),
]
