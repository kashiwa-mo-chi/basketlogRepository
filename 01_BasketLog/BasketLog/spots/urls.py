from django.urls import path
from . import views

app_name = 'spots'

urlpatterns = [
    path('', views.arena_list, name='arena_list'),

    path('<int:arena_id>/', views.arena_top, name='arena_top'),

    path('<int:arena_id>/facility/new/', views.facility_post_create, name='facility_post_create'),
    path('<int:arena_id>/nearby/new/', views.nearby_create, name='nearby_create'),

    path('facility/<int:pk>/', views.facility_detail, name='facility_detail'),
    path('facility/<int:pk>/edit/', views.facility_post_update, name='facility_post_update'),
    path('facility/<int:pk>/delete/', views.facility_post_delete, name='facility_post_delete'),
    path('facility/image/<int:image_pk>/delete/', views.facility_image_delete, name='facility_image_delete'),
    
    path('<int:arena_id>/nearby/', views.nearby_list, name='nearby_list'),
    path('nearby/<int:pk>/', views.nearby_detail, name='nearby_detail'),
    path('nearby/<int:pk>/update/', views.nearby_update, name='nearby_update'),
    path('nearby/<int:pk>/delete/', views.nearby_delete, name='nearby_delete'),
    path('nearby/image/<int:image_pk>/delete/', views.nearby_image_delete, name='nearby_image_delete'),
]
