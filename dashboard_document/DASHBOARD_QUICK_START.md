# Dashboard System - Quick Start Checklist

## 🚀 Fast Setup for New Websites

Use this checklist to quickly replicate the dashboard system on a new website.

---

## 📋 Prerequisites

- [ ] Django project set up
- [ ] Cloudinary account created
- [ ] Database configured (PostgreSQL/MySQL/SQLite)
- [ ] Python 3.8+ installed

---

## ⚡ Quick Setup Steps

### 1. Install Packages

```bash
pip install cloudinary pillow python-dotenv
```

Add to `requirements.txt`:
```txt
cloudinary==1.43.0
pillow==10.4.0
python-dotenv==1.0.1
```

---

### 2. Copy Files

Copy these files from Madrid Marble project:

**Core Files:**
- [ ] `models.py` → `your_app/models.py`
- [ ] `dashboard_views.py` → `your_app/dashboard_views.py`
- [ ] `dashboard_urls.py` → `your_app/dashboard_urls.py`
- [ ] `content_helpers.py` → `your_app/content_helpers.py`
- [ ] `admin.py` → `your_app/admin.py`

**Utilities:**
- [ ] `utils/cloudinary_utils.py` → `your_app/utils/cloudinary_utils.py`
- [ ] `utils/__init__.py` → `your_app/utils/__init__.py`

**Management Command:**
- [ ] `management/commands/import_homepage_data.py` → `your_app/management/commands/import_homepage_data.py`
- [ ] `management/__init__.py` → `your_app/management/__init__.py`
- [ ] `management/commands/__init__.py` → `your_app/management/commands/__init__.py`

**Templates:**
- [ ] `templates/dashboard/base.html` → `your_app/templates/dashboard/base.html`
- [ ] `templates/dashboard/login.html` → `your_app/templates/dashboard/login.html`
- [ ] `templates/dashboard/index.html` → `your_app/templates/dashboard/index.html`
- [ ] `templates/dashboard/gallery.html` → `your_app/templates/dashboard/gallery.html`
- [ ] All other `templates/dashboard/*.html` files

---

### 3. Update Settings

**In `settings.py`:**

Add imports:
```python
import os
from dotenv import load_dotenv
load_dotenv()
```

Add Cloudinary config:
```python
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', ''),
    api_key=os.getenv('CLOUDINARY_API_KEY', ''),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', ''),
    secure=True
)
```

Add auth settings:
```python
LOGIN_URL = '/dashboard/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/dashboard/login/'
```

---

### 4. Update URLs

**In `urls.py`:**

```python
from django.urls import path, include

urlpatterns = [
    # ... existing URLs ...
    path('dashboard/', include('your_app.dashboard_urls')),
    # ... rest of URLs ...
]
```

---

### 5. Update Homepage View

**In `views.py`:**

```python
from django.shortcuts import render
from .content_helpers import get_homepage_content_from_db
from .content.homepage import get_homepage_content  # Fallback

def home(request):
    try:
        content = get_homepage_content_from_db()
    except:
        content = get_homepage_content()  # Fallback to JSON
    return render(request, "home.html", {"content": content})
```

---

### 6. Create .env File

Create `.env` in project root:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

Add to `.gitignore`:
```
.env
```

---

### 7. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 8. Create Superuser

```bash
python manage.py createsuperuser
```

---

### 9. Import Data (Optional)

If you have existing JSON data:

```bash
python manage.py import_homepage_data
```

**Note:** Update `import_homepage_data.py` to match your JSON structure.

---

### 10. Test Dashboard

1. Run server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to: `http://localhost:8000/dashboard/`

3. Log in with superuser credentials

4. Test image upload:
   - Go to Gallery
   - Upload an image
   - Verify it appears

5. Test content editing:
   - Edit a section (e.g., Hero)
   - Save changes
   - Verify on website

---

## 🎨 Customization

### Change Colors

Update `base.html`:
```html
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
```

### Change Brand Name

Update sidebar in `base.html`:
```html
<h1 class="text-2xl font-bold mb-8">Your Brand Name</h1>
```

### Change Logo

Update `navigation_edit.html` and `footer_edit.html` templates.

---

## 🔧 Troubleshooting

### Images Not Uploading
- [ ] Check Cloudinary credentials in `.env`
- [ ] Verify Cloudinary account is active
- [ ] Check file size (max 10MB)

### Database Errors
- [ ] Run migrations: `python manage.py migrate`
- [ ] Check database connection
- [ ] Verify all models are registered

### Authentication Issues
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Verify user is active
- [ ] Check session settings

---

## ✅ Completion Checklist

- [ ] All files copied
- [ ] Settings updated
- [ ] URLs configured
- [ ] Homepage view updated
- [ ] Environment variables set
- [ ] Migrations run
- [ ] Superuser created
- [ ] Data imported (if needed)
- [ ] Dashboard tested
- [ ] Image upload tested
- [ ] Content editing tested
- [ ] Customization complete

---

## 🚀 Ready to Go!

Once all steps are complete, your dashboard is ready to use!

**Next Steps:**
1. Customize branding/colors
2. Add your content
3. Upload images
4. Test all functionality
5. Deploy to production

---

## 📚 Reference

- **Full Guide**: See `DASHBOARD_REPLICATION_GUIDE.md` for detailed instructions
- **Documentation**: See `DASHBOARD_README.md` for usage documentation
- **Django Docs**: https://docs.djangoproject.com/
- **Cloudinary Docs**: https://cloudinary.com/documentation

---

**Happy Coding! 🎉**

