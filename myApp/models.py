from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import json


class MediaAsset(models.Model):
    """Cloudinary image asset - stores URLs only, no file storage"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    public_id = models.CharField(max_length=255, unique=True)
    secure_url = models.URLField(max_length=500)
    web_url = models.URLField(max_length=500, help_text="Optimized variant: f_auto,q_auto")
    thumb_url = models.URLField(max_length=500, help_text="Thumbnail variant: c_fill,g_face,w_480,h_320")
    bytes_size = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    format = models.CharField(max_length=10, blank=True)
    tags_csv = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Media Asset"
        verbose_name_plural = "Media Assets"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            base_slug = self.slug
            counter = 1
            while MediaAsset.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def url(self):
        """Returns optimized web URL"""
        return self.web_url or self.secure_url


class SEO(models.Model):
    """SEO metadata for homepage"""
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    canonical = models.URLField(blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.TextField(max_length=300, blank=True)
    og_image = models.URLField(blank=True)
    favicon = models.URLField(blank=True)
    preload_hero = models.URLField(blank=True)

    class Meta:
        verbose_name = "SEO"
        verbose_name_plural = "SEO"

    def __str__(self):
        return "Homepage SEO"


class Navigation(models.Model):
    """Navigation configuration"""
    logo_text = models.CharField(max_length=10, default="MM", help_text="Fallback text if logo image is not provided")
    logo_image_url = models.URLField(max_length=500, blank=True, help_text="Logo image URL (if provided, this will be used instead of logo_text)")
    brand = models.CharField(max_length=100, default="Madrid Marble")
    links_json = models.JSONField(default=list, help_text="Array of {label, href} objects")
    cta_label = models.CharField(max_length=100, blank=True)
    cta_href = models.CharField(max_length=200, default="#contact")

    class Meta:
        verbose_name = "Navigation"
        verbose_name_plural = "Navigation"

    def __str__(self):
        return "Navigation"


class Hero(models.Model):
    """Hero section content"""
    badge = models.CharField(max_length=100, blank=True)
    headline = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    primary_cta_label = models.CharField(max_length=100, blank=True)
    primary_cta_href = models.CharField(max_length=200, default="#contact")
    primary_cta_icon = models.CharField(max_length=50, blank=True)
    secondary_cta_label = models.CharField(max_length=100, blank=True)
    secondary_cta_href = models.CharField(max_length=200, blank=True)
    testimonial_quote = models.TextField(blank=True)
    testimonial_name = models.CharField(max_length=100, blank=True)
    testimonial_meta = models.CharField(max_length=100, blank=True)
    testimonial_stars = models.IntegerField(default=5)

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Hero"

    def __str__(self):
        return "Hero Section"


class About(models.Model):
    """About section content"""
    badge = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    copy_json = models.JSONField(default=list, help_text="Array of paragraph strings")
    gallery_json = models.JSONField(default=list, help_text="Array of {url, alt} objects")

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"

    def __str__(self):
        return "About Section"


class Stat(models.Model):
    """Statistics item"""
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Stat"
        verbose_name_plural = "Stats"

    def __str__(self):
        return f"{self.value} - {self.label}"


class Service(models.Model):
    """Service item in services section"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    is_open = models.BooleanField(default=False, help_text="Open by default in accordion")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class Services(models.Model):
    """Services section configuration"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
    image_alt = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Services Section"
        verbose_name_plural = "Services Section"

    def __str__(self):
        return "Services Section"


class PortfolioProject(models.Model):
    """Portfolio project item"""
    image_url = models.URLField(max_length=500)
    image_alt = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="If unchecked, this project will be hidden from the frontend")

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    """Portfolio section configuration"""
    heading = models.CharField(max_length=200)
    description = models.TextField()
    feature_image_url = models.URLField(max_length=500, blank=True)
    feature_image_alt = models.CharField(max_length=200, blank=True)
    feature_title = models.CharField(max_length=200, blank=True)
    feature_description = models.TextField(blank=True)
    feature_tags_json = models.JSONField(default=list, help_text="Array of tag strings")
    feature_testimonial_quote = models.TextField(blank=True)
    feature_testimonial_author = models.CharField(max_length=200, blank=True)
    feature_cta_label = models.CharField(max_length=100, blank=True)
    feature_cta_href = models.CharField(max_length=200, default="#contact")
    feature_cta_icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Portfolio Section"
        verbose_name_plural = "Portfolio Section"

    def __str__(self):
        return "Portfolio Section"


class Testimonial(models.Model):
    """Testimonial item"""
    quote = models.TextField()
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    avatar = models.URLField(max_length=500, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.role}"


class FAQ(models.Model):
    """FAQ item"""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class FAQSection(models.Model):
    """FAQ section configuration"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    cta_label = models.CharField(max_length=100, blank=True)
    cta_href = models.CharField(max_length=200, default="#contact")
    cta_icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "FAQ Section"
        verbose_name_plural = "FAQ Section"

    def __str__(self):
        return "FAQ Section"


class ContactInfo(models.Model):
    """Contact information item"""
    label = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    href = models.URLField(blank=True, help_text="Optional link (mailto: or tel:)")
    info_type = models.CharField(max_length=20, choices=[
        ('address', 'Address'),
        ('email', 'Email'),
        ('phone', 'Phone'),
    ], default='address')
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return f"{self.label}: {self.text}"


class SocialLink(models.Model):
    """Social media link"""
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    href = models.URLField(max_length=500)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.icon


class Contact(models.Model):
    """Contact section configuration"""
    badge = models.CharField(max_length=100, default="CONTACT")
    heading = models.CharField(max_length=200)
    description = models.TextField()
    intro_text = models.TextField()
    background_image = models.URLField(max_length=500, blank=True)
    socials_label = models.CharField(max_length=100, default="FOLLOW MADRID MARBLE")
    form_submit_label = models.CharField(max_length=100, default="Submit inquiry")
    form_disclaimer = models.TextField(blank=True)

    class Meta:
        verbose_name = "Contact Section"
        verbose_name_plural = "Contact Section"

    def __str__(self):
        return "Contact Section"


class ContactFormField(models.Model):
    """Contact form field configuration"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='form_fields')
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('email', 'Email'),
        ('tel', 'Phone'),
        ('textarea', 'Textarea'),
    ], default='text')
    placeholder = models.CharField(max_length=200)
    span = models.IntegerField(default=1, help_text="Grid span: 1 or 2")
    rows = models.IntegerField(default=5, help_text="For textarea only")
    required = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Contact Form Field"
        verbose_name_plural = "Contact Form Fields"

    def __str__(self):
        return f"{self.contact.heading} - {self.label}"


class Footer(models.Model):
    """Footer configuration"""
    logo_text = models.CharField(max_length=10, default="MM")
    note = models.CharField(max_length=200, default="Madrid Marble. All rights reserved.")
    links_json = models.JSONField(default=list, help_text="Array of {label, href} objects")

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

    def __str__(self):
        return "Footer"
