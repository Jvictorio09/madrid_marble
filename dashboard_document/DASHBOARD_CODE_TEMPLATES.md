# Dashboard System - Code Templates

## 📋 Quick Reference Code Snippets

This document provides code templates for key files. Copy and modify as needed.

---

## 🔧 Settings Configuration

### `settings.py` - Cloudinary Configuration

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloudinary Configuration
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', ''),
    api_key=os.getenv('CLOUDINARY_API_KEY', ''),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', ''),
    secure=True
)

# Login URL for dashboard
LOGIN_URL = '/dashboard/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/dashboard/login/'
```

---

## 🔗 URLs Configuration

### `urls.py` - Main Project URLs

```python
from django.urls import path, include

urlpatterns = [
    # ... your existing URLs ...
    path('dashboard/', include('your_app.dashboard_urls')),
    path('', views.home, name='home'),
    # ... rest of URLs ...
]
```

### `dashboard_urls.py` - Dashboard URLs

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from . import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='dashboard/login.html',
        authentication_form=AuthenticationForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard Home
    path('', dashboard_views.dashboard_home, name='home'),
    
    # Image Upload & Gallery
    path('gallery/', dashboard_views.gallery, name='gallery'),
    path('upload-image/', dashboard_views.upload_image, name='upload_image'),
    
    # Add your section URLs here
    # path('your-section/', dashboard_views.your_section_edit, name='your_section_edit'),
]
```

---

## 🏠 Homepage View

### `views.py` - Updated Homepage View

```python
from django.shortcuts import render
from .content_helpers import get_homepage_content_from_db
from .content.homepage import get_homepage_content  # Fallback to JSON

def home(request):
    """Homepage view - uses database if available, falls back to JSON"""
    try:
        # Try to get content from database
        content = get_homepage_content_from_db()
    except:
        # Fall back to JSON file if database is not set up
        content = get_homepage_content()
    
    context = {
        "content": content
    }
    return render(request, "home.html", context)
```

---

## 📦 Requirements

### `requirements.txt` - Required Packages

```txt
cloudinary==1.43.0
pillow==10.4.0
python-dotenv==1.0.1
Django>=3.2
```

---

## 🔐 Environment Variables

### `.env` - Cloudinary Credentials

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### `.gitignore` - Exclude Environment Variables

```gitignore
.env
*.pyc
__pycache__/
db.sqlite3
media/
staticfiles/
```

---

## 🗄️ Database Models Template

### `models.py` - Basic Model Template

```python
from django.db import models
from django.utils.text import slugify

class YourSection(models.Model):
    """Your section description"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Your Section"
        verbose_name_plural = "Your Sections"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

---

## 🎨 Dashboard Views Template

### `dashboard_views.py` - Basic View Template

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import YourSection

@login_required
def your_section_edit(request):
    """Edit your section"""
    section = YourSection.objects.first()
    if not section:
        section = YourSection.objects.create(
            title="Default Title",
            description="Default description",
        )
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.description = request.POST.get('description', '')
        section.image_url = request.POST.get('image_url', '')
        section.save()
        messages.success(request, 'Section updated successfully!')
        return redirect('dashboard:your_section_edit')
    
    return render(request, 'dashboard/your_section_edit.html', {'section': section})
```

---

## 🖼️ Image Upload View

### `dashboard_views.py` - Image Upload Endpoint

```python
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from .utils.cloudinary_utils import smart_compress_to_bytes, upload_to_cloudinary, TARGET_BYTES
from .models import MediaAsset

@login_required
@require_POST
@csrf_exempt
def upload_image(request):
    """Handle image upload with automatic compression and Cloudinary upload."""
    if 'file' not in request.FILES:
        return JsonResponse({"success": False, "error": "No file provided"})
    
    file = request.FILES['file']
    folder = request.POST.get('folder', 'your_app/uploads')
    tags = request.POST.get('tags', '').split(',') if request.POST.get('tags') else []
    
    try:
        # Compress if needed
        if file.size > TARGET_BYTES:
            file_bytes = smart_compress_to_bytes(file)
        else:
            file_bytes = file.read()
        
        # Generate public_id from filename
        public_id = slugify(file.name.rsplit('.', 1)[0])
        
        # Upload to Cloudinary
        result, web_url, thumb_url = upload_to_cloudinary(
            file_bytes=file_bytes,
            folder=folder,
            public_id=public_id,
            tags=tags
        )
        
        # Store in database
        asset = MediaAsset.objects.create(
            title=file.name,
            public_id=result.get("public_id"),
            secure_url=result.get("secure_url"),
            web_url=web_url,
            thumb_url=thumb_url,
            bytes_size=result.get("bytes", 0),
            width=result.get("width", 0),
            height=result.get("height", 0),
            format=result.get("format", ""),
            tags_csv=",".join(tags) if tags else "",
        )
        
        return JsonResponse({
            "success": True,
            "id": asset.id,
            "title": asset.title,
            "secure_url": asset.secure_url,
            "web_url": asset.web_url,
            "thumb_url": asset.thumb_url,
        })
    
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
```

---

## 📝 Content Helpers Template

### `content_helpers.py` - Database to JSON Conversion

```python
from .models import YourSection

def get_homepage_content_from_db():
    """Convert database models to JSON format for templates"""
    
    # Get or create default instances
    your_section = YourSection.objects.first()
    
    # Build content dictionary
    content = {
        "your_section": {
            "title": your_section.title if your_section else "",
            "description": your_section.description if your_section else "",
            "image_url": your_section.image_url if your_section else "",
        },
        # Add more sections here
    }
    
    return content
```

---

## 🎨 Dashboard Template Template

### `templates/dashboard/base.html` - Base Template

```html
<!DOCTYPE html>
<html lang="en" class="h-full bg-gray-50">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Dashboard - Your Brand{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'beige': { /* your colors */ },
                        'navy': { /* your colors */ }
                    }
                }
            }
        }
    </script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
</head>
<body class="h-full">
    <div class="min-h-full flex">
        <!-- Sidebar -->
        <aside class="w-64 bg-navy-900 text-white flex-shrink-0 relative">
            <div class="p-6 h-full flex flex-col">
                <h1 class="text-2xl font-bold mb-8">Your Brand</h1>
                <nav class="space-y-2 flex-1 overflow-y-auto">
                    <a href="{% url 'dashboard:home' %}" class="block px-4 py-2 rounded hover:bg-navy-800">
                        <i class="fa-solid fa-home mr-2"></i> Dashboard
                    </a>
                    <a href="{% url 'dashboard:gallery' %}" class="block px-4 py-2 rounded hover:bg-navy-800">
                        <i class="fa-solid fa-images mr-2"></i> Gallery
                    </a>
                    <!-- Add more navigation items here -->
                </nav>
                <div class="mt-auto pt-6 border-t border-navy-800">
                    <a href="{% url 'dashboard:logout' %}" class="block px-4 py-2 rounded hover:bg-navy-800 text-red-400">
                        <i class="fa-solid fa-sign-out-alt mr-2"></i> Logout
                    </a>
                </div>
            </div>
        </aside>

        <!-- Main content -->
        <main class="flex-1 overflow-auto">
            <div class="p-8">
                {% if messages %}
                <div class="mb-6">
                    {% for message in messages %}
                    <div class="p-4 rounded-lg mb-2 {% if message.tags == 'success' %}bg-green-100 text-green-800{% elif message.tags == 'error' %}bg-red-100 text-red-800{% else %}bg-blue-100 text-blue-800{% endif %}">
                        {{ message }}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}

                {% block content %}
                {% endblock %}
            </div>
        </main>
    </div>
</body>
</html>
```

---

## 📝 Edit Template Template

### `templates/dashboard/your_section_edit.html` - Edit Page Template

```html
{% extends "dashboard/base.html" %}

{% block title %}Edit Your Section - Dashboard{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-8">
        <h1 class="text-4xl font-bold text-navy-900">Edit Your Section</h1>
        <a href="{% url 'dashboard:home' %}" class="text-gray-600 hover:text-navy-900">
            <i class="fa-solid fa-arrow-left mr-2"></i> Back to Dashboard
        </a>
    </div>

    <form method="post" class="bg-white rounded-xl shadow-sm p-8 space-y-6">
        {% csrf_token %}
        
        <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Title</label>
            <input type="text" name="title" value="{{ section.title|default:'' }}" required
                   placeholder="Your Title"
                   class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-navy-900 focus:outline-none focus:ring-2 focus:ring-navy-900/20">
        </div>

        <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Description</label>
            <textarea name="description" rows="4" required
                      placeholder="Your description"
                      class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-navy-900 focus:outline-none focus:ring-2 focus:ring-navy-900/20">{{ section.description|default:'' }}</textarea>
        </div>

        <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Image URL</label>
            <input type="url" name="image_url" value="{{ section.image_url|default:'' }}" 
                   placeholder="https://res.cloudinary.com/..."
                   class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-navy-900 focus:outline-none focus:ring-2 focus:ring-navy-900/20">
            <p class="text-sm text-gray-500 mt-2">
                <a href="{% url 'dashboard:gallery' %}" target="_blank" class="text-navy-900 hover:underline">
                    <i class="fa-solid fa-images mr-1"></i> Upload image from gallery
                </a>
            </p>
        </div>

        <div class="flex gap-4 pt-6">
            <button type="submit" class="bg-navy-900 text-white px-8 py-3 rounded-xl font-semibold hover:bg-navy-950 transition">
                Save Changes
            </button>
            <a href="{% url 'dashboard:home' %}" class="bg-gray-200 text-gray-700 px-8 py-3 rounded-xl font-semibold hover:bg-gray-300 transition">
                Cancel
            </a>
        </div>
    </form>
</div>
{% endblock %}
```

---

## 🔧 Cloudinary Utils Template

### `utils/cloudinary_utils.py` - Cloudinary Integration

```python
import io
from pathlib import Path
from PIL import Image, ImageOps
import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

MAX_BYTES = 10 * 1024 * 1024  # 10MB
TARGET_BYTES = int(MAX_BYTES * 0.93)  # 9.3MB target

def smart_compress_to_bytes(src_file) -> bytes:
    """Compress image to target size with WebP conversion."""
    if isinstance(src_file, (str, Path)):
        im = Image.open(src_file)
    else:
        im = Image.open(src_file)

    with im:
        # Auto-rotate based on EXIF
        im = ImageOps.exif_transpose(im)
        
        # Determine format
        fmt = (im.format or "JPEG").upper()
        prefer_webp = fmt in ("PNG", "TIFF")
        out_fmt = "WEBP" if prefer_webp else ("JPEG" if fmt != "WEBP" else "WEBP")
        
        # Cap extreme dimensions
        max_w = 5000
        if im.width > max_w:
            im = im.resize((max_w, int(im.height * (max_w / im.width))), Image.LANCZOS)
        
        # Iterative quality reduction
        q = 82
        min_q = 50 if out_fmt == "JPEG" else 45
        step = 4
        
        while True:
            buf = io.BytesIO()
            if out_fmt == "JPEG":
                im.save(buf, format="JPEG", quality=q, optimize=True, 
                       progressive=True, subsampling="4:2:0")
            else:
                im.save(buf, format="WEBP", quality=q, method=6)
            
            data = buf.getvalue()
            if len(data) <= TARGET_BYTES or q <= min_q:
                return data
            q = max(min_q, q - step)

def upload_to_cloudinary(file_bytes: bytes, folder: str, public_id: str, tags=None):
    """Upload image to Cloudinary and return URLs."""
    try:
        result = cloudinary.uploader.upload(
            file=io.BytesIO(file_bytes),
            resource_type="image",
            folder=folder or "your_app/uploads",
            public_id=public_id,
            overwrite=True,
            unique_filename=False,
            use_filename=False,
            eager=[{
                "format": "webp",
                "quality": "auto",
                "fetch_format": "auto",
                "crop": "limit",
                "width": 2400
            }],
            tags=(tags or []),
            timeout=120,
        )
        
        secure_url = result.get("secure_url", "")
        
        # Generate URL variants
        if "/upload/" in secure_url:
            web_url = secure_url.replace("/upload/", "/upload/f_auto,q_auto/")
            thumb_url = secure_url.replace("/upload/", "/upload/c_fill,g_face,w_480,h_320/")
        else:
            web_url = secure_url
            thumb_url = secure_url
        
        return result, web_url, thumb_url
    
    except CloudinaryError as e:
        raise Exception(f"Cloudinary upload error: {str(e)}")
    except Exception as e:
        raise Exception(f"Upload error: {str(e)}")
```

---

## 📋 Admin Registration Template

### `admin.py` - Django Admin Registration

```python
from django.contrib import admin
from .models import YourSection

@admin.register(YourSection)
class YourSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['sort_order', 'is_active']
```

---

## 🚀 Management Command Template

### `management/commands/import_data.py` - Data Import Command

```python
from django.core.management.base import BaseCommand
from your_app.models import YourSection

class Command(BaseCommand):
    help = 'Import data into the database'

    def handle(self, *args, **options):
        # Your import logic here
        section, created = YourSection.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'Default Title',
                'description': 'Default description',
            }
        )
        
        if not created:
            section.title = 'Updated Title'
            section.save()
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
```

---

## ✅ Quick Setup Checklist

1. [ ] Copy code templates
2. [ ] Update settings.py
3. [ ] Update urls.py
4. [ ] Update views.py
5. [ ] Create .env file
6. [ ] Run migrations
7. [ ] Create superuser
8. [ ] Test dashboard

---

## 🎯 Customization

### Change Colors

Update Tailwind config in `base.html`:
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'your-color': {
                    50: '#...',
                    100: '#...',
                    // ... more shades
                }
            }
        }
    }
}
```

### Change Brand Name

Update sidebar in `base.html`:
```html
<h1 class="text-2xl font-bold mb-8">Your Brand Name</h1>
```

---

## 📚 Reference

- **Full Guide**: See `DASHBOARD_REPLICATION_GUIDE.md`
- **Quick Start**: See `DASHBOARD_QUICK_START.md`
- **File Structure**: See `DASHBOARD_FILE_STRUCTURE.md`

---

**Copy these templates and customize for your needs!**

