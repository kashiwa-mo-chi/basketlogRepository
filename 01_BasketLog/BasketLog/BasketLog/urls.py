from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from BasketApp import views

urlpatterns = [
    path('',views.portfolio, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('games/', include('games.urls')),
    path('spots/', include('spots.urls')),
    path('portfolio/', views.portfolio, name='portfolio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)