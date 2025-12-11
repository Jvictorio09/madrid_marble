# Website Activity Tracking Guide

## 🎯 Overview

This guide shows how to implement website activity tracking for your Django dashboard. Track:
- **Site Visitors**: Total page views and unique visitors
- **Signups**: User registration/account creation
- **Signins**: User login activity
- **Website Activity**: Page views, popular pages, time-based analytics

---

## 📋 Prerequisites

- Django project with dashboard system
- Database (PostgreSQL, MySQL, or SQLite)
- User authentication system

---

## 🚀 Step-by-Step Implementation

### Step 1: Create Activity Tracking Models

Add these models to your `models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from datetime import timedelta

class Visitor(models.Model):
    """Track website visitors and page views"""
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referer = models.URLField(blank=True)
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10, default='GET')
    session_key = models.CharField(max_length=100, blank=True)
    is_unique = models.BooleanField(default=True, help_text="First visit from this IP in 24 hours")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['path', 'created_at']),
        ]
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"
    
    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class UserSignup(models.Model):
    """Track user signups/registrations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='signup_record')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    referer = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Signup"
        verbose_name_plural = "User Signups"
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class UserSignin(models.Model):
    """Track user login activity"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signin_records')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
        verbose_name = "User Signin"
        verbose_name_plural = "User Signins"
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.user.username} - {status} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class PageView(models.Model):
    """Track individual page views with more detail"""
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='page_views', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    path = models.CharField(max_length=500)
    page_title = models.CharField(max_length=200, blank=True)
    duration = models.IntegerField(default=0, help_text="Time spent on page in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['path', '-created_at']),
        ]
        verbose_name = "Page View"
        verbose_name_plural = "Page Views"
    
    def __str__(self):
        return f"{self.path} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
```

---

### Step 2: Create Middleware for Visitor Tracking

Create `middleware.py` in your app:

```python
from django.utils import timezone
from datetime import timedelta
from .models import Visitor, PageView
import hashlib

class VisitorTrackingMiddleware:
    """Middleware to track website visitors"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip tracking for admin and dashboard pages
        if request.path.startswith('/admin/') or request.path.startswith('/dashboard/'):
            return self.get_response(request)
        
        # Skip tracking for static files
        if any(request.path.startswith(prefix) for prefix in ['/static/', '/media/']):
            return self.get_response(request)
        
        # Get visitor info
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referer = request.META.get('HTTP_REFERER', '')
        path = request.path
        method = request.method
        session_key = request.session.session_key or ''
        
        # Check if this is a unique visitor (first visit from this IP in last 24 hours)
        is_unique = not Visitor.objects.filter(
            ip_address=ip_address,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).exists()
        
        # Create visitor record
        visitor = Visitor.objects.create(
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer,
            path=path,
            method=method,
            session_key=session_key,
            is_unique=is_unique
        )
        
        # Create page view record
        PageView.objects.create(
            visitor=visitor,
            user=request.user if request.user.is_authenticated else None,
            path=path,
            page_title='',  # Can be set via JavaScript
        )
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

---

### Step 3: Track User Signups

Update your user registration view or signal:

**Option A: Using Signals (Recommended)**

Add to `models.py` or create `signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserSignup

@receiver(post_save, sender=User)
def track_user_signup(sender, instance, created, **kwargs):
    """Track new user signups"""
    if created:
        # Get request from thread local if available
        # Or store IP during registration
        UserSignup.objects.create(
            user=instance,
            ip_address='',  # Set this during registration
            user_agent='',
            referer=''
        )
```

**Option B: In Registration View**

```python
from django.contrib.auth import login
from .models import UserSignup

def register_view(request):
    if request.method == 'POST':
        # ... create user logic ...
        user = User.objects.create_user(...)
        
        # Track signup
        UserSignup.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referer=request.META.get('HTTP_REFERER', '')
        )
        
        login(request, user)
        return redirect('dashboard:home')
```

---

### Step 4: Track User Signins

Update your login view to track signins:

**Option A: Custom Login View**

```python
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from .models import UserSignin

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            # Track successful signin
            UserSignin.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True
            )
            return redirect('dashboard:home')
        else:
            # Track failed signin attempt
            try:
                user = User.objects.get(username=username)
                UserSignin.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    success=False
                )
            except User.DoesNotExist:
                pass
            # ... show error ...
```

**Option B: Using Signals**

```python
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models import UserSignin

@receiver(user_logged_in)
def track_successful_login(sender, request, user, **kwargs):
    """Track successful login"""
    UserSignin.objects.create(
        user=user,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        success=True
    )

@receiver(user_login_failed)
def track_failed_login(sender, credentials, request, **kwargs):
    """Track failed login attempt"""
    username = credentials.get('username')
    try:
        user = User.objects.get(username=username)
        UserSignin.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=False
        )
    except User.DoesNotExist:
        pass
```

---

### Step 5: Create Dashboard Analytics Views

Add to `dashboard_views.py`:

```python
from django.shortcuts import render
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Visitor, UserSignup, UserSignin, PageView

@login_required
def analytics_dashboard(request):
    """Main analytics dashboard"""
    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    
    # Total Visitors
    total_visitors = Visitor.objects.count()
    unique_visitors_today = Visitor.objects.filter(
        created_at__date=today,
        is_unique=True
    ).count()
    unique_visitors_7d = Visitor.objects.filter(
        created_at__gte=last_7_days,
        is_unique=True
    ).count()
    unique_visitors_30d = Visitor.objects.filter(
        created_at__gte=last_30_days,
        is_unique=True
    ).count()
    
    # Total Page Views
    total_page_views = PageView.objects.count()
    page_views_today = PageView.objects.filter(created_at__date=today).count()
    page_views_7d = PageView.objects.filter(created_at__gte=last_7_days).count()
    page_views_30d = PageView.objects.filter(created_at__gte=last_30_days).count()
    
    # Signups
    total_signups = UserSignup.objects.count()
    signups_today = UserSignup.objects.filter(created_at__date=today).count()
    signups_7d = UserSignup.objects.filter(created_at__gte=last_7_days).count()
    signups_30d = UserSignup.objects.filter(created_at__gte=last_30_days).count()
    
    # Signins
    total_signins = UserSignin.objects.filter(success=True).count()
    signins_today = UserSignin.objects.filter(
        created_at__date=today,
        success=True
    ).count()
    signins_7d = UserSignin.objects.filter(
        created_at__gte=last_7_days,
        success=True
    ).count()
    signins_30d = UserSignin.objects.filter(
        created_at__gte=last_30_days,
        success=True
    ).count()
    
    # Failed login attempts
    failed_logins_today = UserSignin.objects.filter(
        created_at__date=today,
        success=False
    ).count()
    
    # Popular Pages (last 7 days)
    popular_pages = PageView.objects.filter(
        created_at__gte=last_7_days
    ).values('path').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Recent Activity
    recent_visitors = Visitor.objects.select_related('visitor').order_by('-created_at')[:20]
    recent_signups = UserSignup.objects.select_related('user').order_by('-created_at')[:10]
    recent_signins = UserSignin.objects.select_related('user').order_by('-created_at')[:20]
    
    # Daily stats for chart (last 30 days)
    daily_stats = []
    for i in range(30):
        date = today - timedelta(days=i)
        daily_stats.append({
            'date': date,
            'visitors': Visitor.objects.filter(
                created_at__date=date,
                is_unique=True
            ).count(),
            'page_views': PageView.objects.filter(created_at__date=date).count(),
            'signups': UserSignup.objects.filter(created_at__date=date).count(),
            'signins': UserSignin.objects.filter(
                created_at__date=date,
                success=True
            ).count(),
        })
    daily_stats.reverse()
    
    context = {
        # Totals
        'total_visitors': total_visitors,
        'total_page_views': total_page_views,
        'total_signups': total_signups,
        'total_signins': total_signins,
        
        # Today
        'unique_visitors_today': unique_visitors_today,
        'page_views_today': page_views_today,
        'signups_today': signups_today,
        'signins_today': signins_today,
        'failed_logins_today': failed_logins_today,
        
        # Last 7 days
        'unique_visitors_7d': unique_visitors_7d,
        'page_views_7d': page_views_7d,
        'signups_7d': signups_7d,
        'signins_7d': signins_7d,
        
        # Last 30 days
        'unique_visitors_30d': unique_visitors_30d,
        'page_views_30d': page_views_30d,
        'signups_30d': signups_30d,
        'signins_30d': signins_30d,
        
        # Lists
        'popular_pages': popular_pages,
        'recent_visitors': recent_visitors,
        'recent_signups': recent_signups,
        'recent_signins': recent_signins,
        'daily_stats': daily_stats,
    }
    
    return render(request, 'dashboard/analytics.html', context)
```

---

### Step 6: Create Analytics Dashboard Template

Create `templates/dashboard/analytics.html`:

```html
{% extends "dashboard/base.html" %}

{% block title %}Website Analytics - Dashboard{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto">
    <h1 class="text-4xl font-bold text-navy-900 mb-8">Website Analytics</h1>
    
    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Visitors -->
        <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-4">
                <i class="fa-solid fa-users text-3xl text-navy-900"></i>
                <span class="text-sm text-gray-500">Total</span>
            </div>
            <h3 class="text-3xl font-bold text-navy-900 mb-1">{{ total_visitors|default:0 }}</h3>
            <p class="text-gray-600 text-sm">Total Visitors</p>
            <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="flex justify-between text-xs">
                    <span class="text-gray-500">Today:</span>
                    <span class="font-semibold text-navy-900">{{ unique_visitors_today }}</span>
                </div>
                <div class="flex justify-between text-xs mt-1">
                    <span class="text-gray-500">Last 7 days:</span>
                    <span class="font-semibold text-navy-900">{{ unique_visitors_7d }}</span>
                </div>
            </div>
        </div>
        
        <!-- Total Page Views -->
        <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-4">
                <i class="fa-solid fa-eye text-3xl text-navy-900"></i>
                <span class="text-sm text-gray-500">Total</span>
            </div>
            <h3 class="text-3xl font-bold text-navy-900 mb-1">{{ total_page_views|default:0 }}</h3>
            <p class="text-gray-600 text-sm">Page Views</p>
            <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="flex justify-between text-xs">
                    <span class="text-gray-500">Today:</span>
                    <span class="font-semibold text-navy-900">{{ page_views_today }}</span>
                </div>
                <div class="flex justify-between text-xs mt-1">
                    <span class="text-gray-500">Last 7 days:</span>
                    <span class="font-semibold text-navy-900">{{ page_views_7d }}</span>
                </div>
            </div>
        </div>
        
        <!-- Total Signups -->
        <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-4">
                <i class="fa-solid fa-user-plus text-3xl text-navy-900"></i>
                <span class="text-sm text-gray-500">Total</span>
            </div>
            <h3 class="text-3xl font-bold text-navy-900 mb-1">{{ total_signups|default:0 }}</h3>
            <p class="text-gray-600 text-sm">User Signups</p>
            <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="flex justify-between text-xs">
                    <span class="text-gray-500">Today:</span>
                    <span class="font-semibold text-navy-900">{{ signups_today }}</span>
                </div>
                <div class="flex justify-between text-xs mt-1">
                    <span class="text-gray-500">Last 7 days:</span>
                    <span class="font-semibold text-navy-900">{{ signups_7d }}</span>
                </div>
            </div>
        </div>
        
        <!-- Total Signins -->
        <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-4">
                <i class="fa-solid fa-sign-in-alt text-3xl text-navy-900"></i>
                <span class="text-sm text-gray-500">Total</span>
            </div>
            <h3 class="text-3xl font-bold text-navy-900 mb-1">{{ total_signins|default:0 }}</h3>
            <p class="text-gray-600 text-sm">User Signins</p>
            <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="flex justify-between text-xs">
                    <span class="text-gray-500">Today:</span>
                    <span class="font-semibold text-navy-900">{{ signins_today }}</span>
                </div>
                <div class="flex justify-between text-xs mt-1">
                    <span class="text-gray-500">Last 7 days:</span>
                    <span class="font-semibold text-navy-900">{{ signins_7d }}</span>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Popular Pages -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
        <h2 class="text-2xl font-bold text-navy-900 mb-4">Popular Pages (Last 7 Days)</h2>
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Page</th>
                        <th class="px-4 py-3 text-right text-sm font-semibold text-gray-700">Views</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                    {% for page in popular_pages %}
                    <tr class="hover:bg-gray-50">
                        <td class="px-4 py-3 text-sm text-gray-900">{{ page.path }}</td>
                        <td class="px-4 py-3 text-sm text-gray-600 text-right">{{ page.views }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="2" class="px-4 py-8 text-center text-gray-500">No page views yet</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Recent Visitors -->
        <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-xl font-bold text-navy-900 mb-4">Recent Visitors</h2>
            <div class="space-y-3 max-h-96 overflow-y-auto">
                {% for visitor in recent_visitors %}
                <div class="border-b border-gray-100 pb-3">
                    <div class="flex justify-between items-start">
                        <div>
                            <p class="text-sm font-semibold text-navy-900">{{ visitor.path|truncatechars:30 }}</p>
                            <p class="text-xs text-gray-500">{{ visitor.ip_address }}</p>
                        </div>
                        <span class="text-xs text-gray-400">{{ visitor.created_at|timesince }} ago</span>
                    </div>
                </div>
                {% empty %}
                <p class="text-sm text-gray-500">No visitors yet</p>
                {% endfor %}
            </div>
        </div>
        
        <!-- Recent Signups -->
        <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-xl font-bold text-navy-900 mb-4">Recent Signups</h2>
            <div class="space-y-3 max-h-96 overflow-y-auto">
                {% for signup in recent_signups %}
                <div class="border-b border-gray-100 pb-3">
                    <div class="flex justify-between items-start">
                        <div>
                            <p class="text-sm font-semibold text-navy-900">{{ signup.user.username }}</p>
                            <p class="text-xs text-gray-500">{{ signup.user.email }}</p>
                        </div>
                        <span class="text-xs text-gray-400">{{ signup.created_at|timesince }} ago</span>
                    </div>
                </div>
                {% empty %}
                <p class="text-sm text-gray-500">No signups yet</p>
                {% endfor %}
            </div>
        </div>
        
        <!-- Recent Signins -->
        <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-xl font-bold text-navy-900 mb-4">Recent Signins</h2>
            <div class="space-y-3 max-h-96 overflow-y-auto">
                {% for signin in recent_signins %}
                <div class="border-b border-gray-100 pb-3">
                    <div class="flex justify-between items-start">
                        <div>
                            <p class="text-sm font-semibold text-navy-900">
                                {{ signin.user.username }}
                                {% if not signin.success %}
                                <span class="text-red-600 text-xs">(Failed)</span>
                                {% endif %}
                            </p>
                            <p class="text-xs text-gray-500">{{ signin.ip_address }}</p>
                        </div>
                        <span class="text-xs text-gray-400">{{ signin.created_at|timesince }} ago</span>
                    </div>
                </div>
                {% empty %}
                <p class="text-sm text-gray-500">No signins yet</p>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

### Step 7: Add URLs

Add to `dashboard_urls.py`:

```python
path('analytics/', dashboard_views.analytics_dashboard, name='analytics'),
```

---

### Step 8: Add to Sidebar Navigation

Add to `templates/dashboard/base.html` sidebar:

```html
<a href="{% url 'dashboard:analytics' %}" class="block px-4 py-2 rounded hover:bg-navy-800">
    <i class="fa-solid fa-chart-line mr-2"></i> Website Analytics
</a>
```

---

### Step 9: Update Settings

Add middleware to `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware ...
    'myApp.middleware.VisitorTrackingMiddleware',
    # ... rest of middleware ...
]
```

**Important:** Place it after `SessionMiddleware` but before view middleware.

---

### Step 10: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📊 Key Metrics Explained

### Site Visitors
- **Total Visitors**: All visitor records (includes repeat visits)
- **Unique Visitors**: First visit from an IP address in 24 hours
- **Page Views**: Total number of pages viewed

### Signups
- **Total Signups**: All user registrations
- **Daily Signups**: New users registered today
- **Weekly/Monthly**: Signups in last 7/30 days

### Signins
- **Total Signins**: All successful login attempts
- **Daily Signins**: Logins today
- **Failed Logins**: Unsuccessful login attempts (security monitoring)

### Website Activity
- **Popular Pages**: Most viewed pages
- **Recent Activity**: Latest visitors, signups, signins
- **Time-based Stats**: Daily/weekly/monthly trends

---

## 🔧 Customization

### Change Unique Visitor Window

In `middleware.py`, modify the timedelta:

```python
# Change from 24 hours to 1 hour
is_unique = not Visitor.objects.filter(
    ip_address=ip_address,
    created_at__gte=timezone.now() - timedelta(hours=1)
).exists()
```

### Add More Tracking Fields

Add fields to models:

```python
class Visitor(models.Model):
    # ... existing fields ...
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)
```

### Export Analytics Data

Create a management command to export analytics:

```python
# management/commands/export_analytics.py
from django.core.management.base import BaseCommand
from myApp.models import Visitor, UserSignup, UserSignin, PageView
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {
            'visitors': list(Visitor.objects.values()),
            'signups': list(UserSignup.objects.values()),
            'signins': list(UserSignin.objects.values()),
            'page_views': list(PageView.objects.values()),
        }
        with open('analytics_export.json', 'w') as f:
            json.dump(data, f, indent=2, default=str)
        self.stdout.write(self.style.SUCCESS('Analytics exported!'))
```

---

## 🚨 Performance Considerations

### Database Indexing
The models include indexes for common queries. For high-traffic sites, consider:
- Adding more indexes based on query patterns
- Using database partitioning for large tables
- Archiving old data regularly

### Caching
Cache frequently accessed stats:

```python
from django.core.cache import cache

def get_daily_stats():
    cache_key = 'daily_stats'
    stats = cache.get(cache_key)
    if not stats:
        stats = calculate_daily_stats()
        cache.set(cache_key, stats, 300)  # Cache for 5 minutes
    return stats
```

### Cleanup Old Data
Create a management command to archive old records:

```python
# management/commands/cleanup_old_analytics.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from myApp.models import Visitor, PageView

class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=365)
        deleted = Visitor.objects.filter(created_at__lt=cutoff_date).delete()
        self.stdout.write(f'Deleted {deleted[0]} old visitor records')
```

---

## ✅ Testing Checklist

- [ ] Visitor tracking middleware works
- [ ] Unique visitors are counted correctly
- [ ] Page views are recorded
- [ ] User signups are tracked
- [ ] User signins are tracked (success and failure)
- [ ] Analytics dashboard displays all metrics
- [ ] Popular pages list works
- [ ] Recent activity shows correctly
- [ ] Database indexes are created
- [ ] Performance is acceptable

---

## 🎉 Conclusion

You now have a complete website activity tracking system that shows:
- ✅ Total site visitors and unique visitors
- ✅ Total page views
- ✅ User signups
- ✅ User signins (successful and failed)
- ✅ Popular pages
- ✅ Recent activity
- ✅ Time-based analytics

**Next Steps:**
1. Run migrations
2. Add middleware to settings
3. Test tracking
4. View analytics in dashboard
5. Customize as needed

**Happy Tracking! 📊**


