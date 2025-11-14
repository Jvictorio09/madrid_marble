# Dashboard System - File Structure Reference

## 📁 Complete File Structure

This document lists all files needed to replicate the dashboard system.

---

## 🗂️ Directory Structure

```
your_project/
├── your_app/
│   ├── __init__.py
│   ├── models.py                    # ✅ REQUIRED - All database models
│   ├── views.py                     # ✅ REQUIRED - Homepage view (updated)
│   ├── admin.py                     # ✅ REQUIRED - Django admin registration
│   ├── dashboard_views.py           # ✅ REQUIRED - All dashboard views
│   ├── dashboard_urls.py            # ✅ REQUIRED - Dashboard URL routes
│   ├── content_helpers.py           # ✅ REQUIRED - Database to JSON conversion
│   ├── apps.py
│   ├── tests.py
│   │
│   ├── utils/                       # ✅ REQUIRED - Utility functions
│   │   ├── __init__.py
│   │   └── cloudinary_utils.py      # ✅ REQUIRED - Cloudinary integration
│   │
│   ├── management/                  # ✅ REQUIRED - Management commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── import_homepage_data.py  # ✅ REQUIRED - Data import command
│   │
│   ├── templates/
│   │   └── dashboard/               # ✅ REQUIRED - Dashboard templates
│   │       ├── base.html            # ✅ REQUIRED - Base template with sidebar
│   │       ├── login.html           # ✅ REQUIRED - Login page
│   │       ├── index.html           # ✅ REQUIRED - Dashboard homepage
│   │       ├── gallery.html         # ✅ REQUIRED - Image gallery
│   │       │
│   │       ├── seo_edit.html        # ✅ REQUIRED - SEO settings
│   │       ├── navigation_edit.html # ✅ REQUIRED - Navigation settings
│   │       ├── hero_edit.html       # ✅ REQUIRED - Hero section
│   │       ├── about_edit.html      # ✅ REQUIRED - About section
│   │       │
│   │       ├── stats_list.html      # ✅ REQUIRED - Stats list
│   │       ├── stat_edit.html       # ✅ REQUIRED - Stat edit
│   │       │
│   │       ├── services_section_edit.html  # ✅ REQUIRED - Services section
│   │       ├── services_list.html   # ✅ REQUIRED - Services list
│   │       ├── service_edit.html    # ✅ REQUIRED - Service edit
│   │       │
│   │       ├── portfolio_edit.html  # ✅ REQUIRED - Portfolio section
│   │       ├── portfolio_projects_list.html  # ✅ REQUIRED - Projects list
│   │       ├── portfolio_project_edit.html  # ✅ REQUIRED - Project edit
│   │       │
│   │       ├── testimonials_list.html  # ✅ REQUIRED - Testimonials list
│   │       ├── testimonial_edit.html   # ✅ REQUIRED - Testimonial edit
│   │       │
│   │       ├── faq_section_edit.html   # ✅ REQUIRED - FAQ section
│   │       ├── faqs_list.html          # ✅ REQUIRED - FAQs list
│   │       ├── faq_edit.html           # ✅ REQUIRED - FAQ edit
│   │       │
│   │       ├── contact_edit.html       # ✅ REQUIRED - Contact section
│   │       ├── contact_info_list.html  # ✅ REQUIRED - Contact info list
│   │       ├── contact_info_edit.html  # ✅ REQUIRED - Contact info edit
│   │       ├── contact_form_fields_list.html  # ✅ REQUIRED - Form fields list
│   │       ├── contact_form_field_edit.html   # ✅ REQUIRED - Form field edit
│   │       ├── social_links_list.html  # ✅ REQUIRED - Social links list
│   │       ├── social_link_edit.html   # ✅ REQUIRED - Social link edit
│   │       │
│   │       └── footer_edit.html       # ✅ REQUIRED - Footer settings
│   │
│   └── content/                      # ⚠️ OPTIONAL - JSON fallback
│       ├── __init__.py
│       ├── homepage.json
│       └── homepage.py
│
├── your_project/
│   ├── __init__.py
│   ├── settings.py                   # ✅ REQUIRED - Updated with Cloudinary
│   ├── urls.py                       # ✅ REQUIRED - Updated with dashboard URLs
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py
├── requirements.txt                  # ✅ REQUIRED - Updated with packages
├── .env                              # ✅ REQUIRED - Cloudinary credentials
└── .gitignore                        # ✅ REQUIRED - Add .env
```

---

## 📄 File Descriptions

### Core Files

#### `models.py`
- **Purpose**: Database models for all content sections
- **Key Models**: MediaAsset, SEO, Navigation, Hero, About, Stat, Service, Portfolio, Testimonial, FAQ, Contact, Footer
- **Required**: Yes

#### `dashboard_views.py`
- **Purpose**: All dashboard views and CRUD operations
- **Key Views**: dashboard_home, upload_image, gallery, *_edit, *_list, *_delete
- **Required**: Yes

#### `dashboard_urls.py`
- **Purpose**: URL routes for dashboard
- **Key Routes**: /dashboard/, /dashboard/login/, /dashboard/gallery/, etc.
- **Required**: Yes

#### `content_helpers.py`
- **Purpose**: Converts database models to JSON format for templates
- **Key Function**: get_homepage_content_from_db()
- **Required**: Yes

#### `admin.py`
- **Purpose**: Django admin registration for all models
- **Required**: Yes

### Utility Files

#### `utils/cloudinary_utils.py`
- **Purpose**: Cloudinary integration and image processing
- **Key Functions**: smart_compress_to_bytes(), upload_to_cloudinary()
- **Required**: Yes

### Management Commands

#### `management/commands/import_homepage_data.py`
- **Purpose**: Imports JSON data into database
- **Usage**: `python manage.py import_homepage_data`
- **Required**: Optional (only if importing existing data)

### Templates

#### `templates/dashboard/base.html`
- **Purpose**: Base template with sidebar navigation
- **Features**: Tailwind CSS, Font Awesome icons, responsive design
- **Required**: Yes

#### `templates/dashboard/login.html`
- **Purpose**: Login page
- **Required**: Yes

#### `templates/dashboard/index.html`
- **Purpose**: Dashboard homepage with overview cards
- **Required**: Yes

#### `templates/dashboard/gallery.html`
- **Purpose**: Image gallery with upload functionality
- **Required**: Yes

#### All Other Templates
- **Purpose**: Edit and list pages for each content section
- **Required**: Yes

### Configuration Files

#### `settings.py`
- **Updates Needed**:
  - Cloudinary configuration
  - Authentication settings
  - Static files configuration
- **Required**: Yes (update existing)

#### `urls.py`
- **Updates Needed**:
  - Add dashboard URLs
- **Required**: Yes (update existing)

#### `views.py`
- **Updates Needed**:
  - Update homepage view to use database
- **Required**: Yes (update existing)

#### `requirements.txt`
- **Updates Needed**:
  - Add cloudinary, pillow, python-dotenv
- **Required**: Yes (update existing)

#### `.env`
- **Purpose**: Environment variables for Cloudinary
- **Required**: Yes (create new)

---

## 🔄 File Dependencies

### Database Models → Views → URLs → Templates

```
models.py
    ↓
dashboard_views.py (uses models)
    ↓
dashboard_urls.py (uses views)
    ↓
templates/dashboard/*.html (uses views)
```

### Cloudinary Integration

```
utils/cloudinary_utils.py
    ↓
dashboard_views.py (uses cloudinary_utils)
    ↓
templates/dashboard/gallery.html (uses upload view)
```

### Content Helpers

```
models.py
    ↓
content_helpers.py (converts models to JSON)
    ↓
views.py (uses content_helpers)
    ↓
templates/home.html (uses JSON)
```

---

## 📋 Copy Checklist

### Required Files (Copy As-Is)

- [ ] `models.py`
- [ ] `dashboard_views.py`
- [ ] `dashboard_urls.py`
- [ ] `content_helpers.py`
- [ ] `admin.py`
- [ ] `utils/cloudinary_utils.py`
- [ ] `utils/__init__.py`
- [ ] `templates/dashboard/base.html`
- [ ] `templates/dashboard/login.html`
- [ ] `templates/dashboard/index.html`
- [ ] `templates/dashboard/gallery.html`
- [ ] All other `templates/dashboard/*.html` files

### Files to Update (Modify Existing)

- [ ] `settings.py` (add Cloudinary config)
- [ ] `urls.py` (add dashboard URLs)
- [ ] `views.py` (update homepage view)
- [ ] `requirements.txt` (add packages)

### Files to Create (New)

- [ ] `.env` (Cloudinary credentials)
- [ ] `management/commands/import_homepage_data.py` (optional)

---

## 🎯 Quick Copy Command

If you're copying from Madrid Marble project:

```bash
# Copy core files
cp myApp/models.py your_app/models.py
cp myApp/dashboard_views.py your_app/dashboard_views.py
cp myApp/dashboard_urls.py your_app/dashboard_urls.py
cp myApp/content_helpers.py your_app/content_helpers.py
cp myApp/admin.py your_app/admin.py

# Copy utils
cp -r myApp/utils your_app/

# Copy management commands
cp -r myApp/management your_app/

# Copy templates
cp -r myApp/templates/dashboard your_app/templates/
```

---

## ✅ Verification Checklist

After copying files, verify:

- [ ] All models are in `models.py`
- [ ] All views are in `dashboard_views.py`
- [ ] All URLs are in `dashboard_urls.py`
- [ ] All templates are in `templates/dashboard/`
- [ ] Cloudinary utils are in `utils/cloudinary_utils.py`
- [ ] Settings are updated with Cloudinary config
- [ ] URLs are updated with dashboard routes
- [ ] Homepage view is updated
- [ ] Environment variables are set
- [ ] All imports are correct

---

## 🚀 Next Steps

1. Copy all required files
2. Update configuration files
3. Run migrations
4. Create superuser
5. Test dashboard
6. Customize as needed

---

**Reference this document when setting up the dashboard on a new website!**

