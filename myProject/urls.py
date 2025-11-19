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
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
