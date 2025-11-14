# Madrid Marble Dashboard

A comprehensive WordPress-like content management system for the Madrid Marble website. This dashboard allows non-technical users to manage all website content, upload images via Cloudinary, and edit all homepage sections without touching code.

## Features

### 🎯 Complete Content Management
- **SEO Settings**: Manage meta tags, Open Graph data, and canonical URLs
- **Navigation**: Edit logo, brand name, menu links, and CTA buttons
- **Hero Section**: Edit headline, description, images, CTAs, and testimonials
- **About Section**: Manage content, gallery images, and copy
- **Stats**: Add, edit, and reorder statistics
- **Services**: Manage services with icons and descriptions
- **Portfolio**: Edit featured project and manage portfolio projects
- **Testimonials**: Add and manage customer testimonials
- **FAQs**: Manage frequently asked questions
- **Contact**: Edit contact section, info, form fields, and social links
- **Footer**: Edit footer content and links

### 🖼️ Image Management
- **Cloudinary Integration**: Upload images directly to Cloudinary
- **Automatic Compression**: Images are automatically compressed before upload
- **WebP Conversion**: Images are automatically converted to WebP for optimal performance
- **Image Gallery**: Browse all uploaded images, copy URLs, and manage assets
- **Optimized URLs**: Multiple URL variants (original, web-optimized, thumbnail)

### 🔐 Authentication
- **Login/Logout**: Secure authentication system
- **Protected Routes**: All dashboard routes require authentication
- **Session Management**: Django session-based authentication

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Cloudinary

Add your Cloudinary credentials to your `.env` file:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 3. Create Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Import Existing Data (Optional)

If you have existing JSON data, import it into the database:

```bash
python manage.py import_homepage_data
```

### 5. Create Superuser

Create a superuser account to access the dashboard:

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

### 7. Access Dashboard

Navigate to `http://localhost:8000/dashboard/` and log in with your superuser credentials.

## Usage

### Accessing the Dashboard

1. Navigate to `/dashboard/`
2. Log in with your superuser credentials
3. Use the sidebar to navigate to different sections

### Uploading Images

1. Go to **Gallery** in the sidebar
2. Click **Upload Image**
3. Select an image file (max 10MB)
4. Optionally set a folder and tags
5. Click **Upload**

The image will be automatically compressed and uploaded to Cloudinary. You'll receive multiple URL variants:
- **secure_url**: Original uploaded image
- **web_url**: Web-optimized variant (auto format & quality)
- **thumb_url**: Thumbnail variant (480x320, face detection)

### Editing Content

1. Navigate to the section you want to edit (e.g., **Hero**, **About**, **Contact**)
2. Edit the fields
3. Click **Save Changes**
4. Changes are immediately reflected on the website

### Managing Lists (Stats, Services, FAQs, etc.)

1. Navigate to the list view (e.g., **Stats**, **Services**)
2. Click **Add [Item]** to create a new item
3. Click **Edit** to modify an existing item
4. Click **Delete** to remove an item
5. Use **Sort Order** to control the display order

## Database Models

### Core Models

- **SEO**: SEO metadata for homepage
- **Navigation**: Navigation menu configuration
- **Hero**: Hero section content
- **About**: About section content
- **Stat**: Statistics items
- **Service**: Service items
- **Services**: Services section configuration
- **Portfolio**: Portfolio section configuration
- **PortfolioProject**: Portfolio project items
- **Testimonial**: Testimonial items
- **FAQ**: FAQ items
- **FAQSection**: FAQ section configuration
- **Contact**: Contact section configuration
- **ContactInfo**: Contact information items
- **ContactFormField**: Contact form field configurations
- **SocialLink**: Social media links
- **Footer**: Footer configuration
- **MediaAsset**: Cloudinary image assets

## Cloudinary Image Processing

### Automatic Compression

Images are automatically compressed before upload:
- **Max Size**: 10MB
- **Target Size**: 9.3MB (93% of max)
- **Format Conversion**: PNG/TIFF → WebP, JPEG → JPEG
- **Dimension Capping**: Max width 5000px
- **Quality Optimization**: Iterative quality reduction

### URL Variants

After upload, multiple URL variants are generated:
- **web_url**: `f_auto,q_auto` (auto format & quality)
- **thumb_url**: `c_fill,g_face,w_480,h_320` (thumbnail with face detection)
- **secure_url**: Original uploaded image

### URL Transformations

Cloudinary supports URL-based transformations (no re-uploads):
- **Format**: `f_auto`, `f_webp`, `f_jpg`
- **Quality**: `q_auto`, `q_80`, `q_60`
- **Dimensions**: `w_2400`, `h_1350`, `c_limit`, `c_fill`
- **Gravity**: `g_face`, `g_auto`, `g_center`

## API Endpoints

### Image Upload

**POST** `/dashboard/upload-image/`

**Request:**
- `file`: Image file (required)
- `folder`: Cloudinary folder (optional)
- `tags`: Comma-separated tags (optional)

**Response:**
```json
{
  "success": true,
  "id": 1,
  "title": "image.jpg",
  "secure_url": "https://res.cloudinary.com/...",
  "web_url": "https://res.cloudinary.com/.../f_auto,q_auto/...",
  "thumb_url": "https://res.cloudinary.com/.../c_fill,g_face,w_480,h_320/...",
  "public_id": "madrid_marble/uploads/image",
  "width": 1920,
  "height": 1080,
  "format": "jpg",
  "bytes": 2456789
}
```

## Troubleshooting

### Images Not Uploading

1. Check Cloudinary credentials in `.env`
2. Verify Cloudinary account is active
3. Check file size (max 10MB)
4. Verify network connection

### Database Errors

1. Run migrations: `python manage.py migrate`
2. Check database connection in `settings.py`
3. Verify PostgreSQL is running

### Authentication Issues

1. Create superuser: `python manage.py createsuperuser`
2. Verify user is active in Django admin
3. Check session settings in `settings.py`

## Security

- All dashboard routes require authentication
- CSRF protection enabled
- Secure password validation
- Session-based authentication
- Cloudinary secure URLs (HTTPS)

## Performance

- Images are automatically compressed before upload
- WebP conversion for optimal file sizes
- Cloudinary CDN for fast image delivery
- Database queries are optimized
- Static files are served efficiently

## Support

For issues or questions, please contact the development team.

---

**Built with Django, Cloudinary, and Tailwind CSS**

