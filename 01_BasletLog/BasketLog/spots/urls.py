from django.urls import path
from . import views

app_name = 'spots'

urlpatterns = [
    path('', views.spot_top, name='spot_top'),
    path('facility/new/', views.facility_post_create, name='facility_post_create'),
    path('nearby/new/', views.nearby_post_create, name='nearby_post_create'),
]
