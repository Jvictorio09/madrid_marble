from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('myApp.dashboard_urls')),
    path('', views.home, name='home'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
