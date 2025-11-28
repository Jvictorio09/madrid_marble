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
    eyebrow = models.CharField(max_length=200, blank=True, help_text="Text above headline (e.g., 'Premium Marble Works for Homes, Hotels...')")
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
    stats_json = models.JSONField(default=list, blank=True, help_text="Array of {value, label, description} objects for hero stats")

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
    href = models.URLField(blank=True, help_text="Optional link (mailto:, tel:, or https://wa.me/)")
    info_type = models.CharField(max_length=20, choices=[
        ('address', 'Address'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
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


class PromiseCard(models.Model):
    """Promise section card item"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., 'fa-solid fa-gem')")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Promise Card"
        verbose_name_plural = "Promise Cards"

    def __str__(self):
        return self.title


class Promise(models.Model):
    """Our Promise section configuration"""
    title = models.CharField(max_length=200, default="Our Promise")
    main_statement = models.TextField(help_text="Main promise statement")
    substatement = models.TextField(blank=True, help_text="Supporting statement")
    closing_statement = models.TextField(blank=True, help_text="Closing statement (italic text)")

    class Meta:
        verbose_name = "Promise Section"
        verbose_name_plural = "Promise Section"

    def __str__(self):
        return "Promise Section"


class FeaturedService(models.Model):
    """Featured service item"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Featured Service"
        verbose_name_plural = "Featured Services"

    def __str__(self):
        return self.title


class FeaturedServices(models.Model):
    """Featured Services section configuration"""
    title = models.CharField(max_length=200, default="Featured Services")
    description = models.TextField()

    class Meta:
        verbose_name = "Featured Services Section"
        verbose_name_plural = "Featured Services Section"

    def __str__(self):
        return "Featured Services Section"


class WhyTrustFactor(models.Model):
    """Why Clients Trust Us factor item"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Why Trust Factor"
        verbose_name_plural = "Why Trust Factors"

    def __str__(self):
        return self.title


class WhyTrust(models.Model):
    """Why Clients Trust Us section configuration"""
    title = models.CharField(max_length=200, default="Why Clients Trust Madrid Marble")
    subtitle = models.TextField(blank=True, help_text="Subtitle/description")

    class Meta:
        verbose_name = "Why Trust Section"
        verbose_name_plural = "Why Trust Section"

    def __str__(self):
        return "Why Trust Section"


# Individual Page Models
class AboutPage(models.Model):
    """About Page content"""
    # Hero Section
    badge = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    intro_paragraph_1 = models.TextField()
    intro_paragraph_2 = models.TextField()
    hero_image_url = models.URLField(max_length=500, blank=True)
    hero_image_alt = models.CharField(max_length=200, blank=True)
    since_badge = models.CharField(max_length=50, blank=True, help_text="e.g., 'Since 20XX'")
    
    # Story Timeline
    story_title = models.CharField(max_length=200, blank=True)
    story_description = models.TextField(blank=True)
    
    # Mission & Philosophy
    mission_title = models.CharField(max_length=200, blank=True)
    mission_description = models.TextField(blank=True)
    
    # What Sets Us Apart
    sets_apart_title = models.CharField(max_length=200, blank=True)
    sets_apart_description = models.TextField(blank=True)
    
    # Workshop Section
    workshop_badge = models.CharField(max_length=100, blank=True)
    workshop_title = models.CharField(max_length=200, blank=True)
    workshop_description = models.TextField(blank=True)
    workshop_image_url = models.URLField(max_length=500, blank=True)
    workshop_image_alt = models.CharField(max_length=200, blank=True)
    workshop_stats_json = models.JSONField(default=list, blank=True, help_text="Array of {value, label, description} objects")
    
    # Our Values
    values_title = models.CharField(max_length=200, blank=True)
    values_description = models.TextField(blank=True)
    
    # Meet the Team
    team_title = models.CharField(max_length=200, blank=True)
    team_description = models.TextField(blank=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page"


class AboutTimelineItem(models.Model):
    """About Page timeline item"""
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='timeline_items')
    period = models.CharField(max_length=100, help_text="e.g., 'The early workshop days'")
    description = models.TextField()
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Timeline Item"
        verbose_name_plural = "Timeline Items"

    def __str__(self):
        return self.period


class AboutMissionCard(models.Model):
    """About Page mission/philosophy card"""
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='mission_cards')
    label = models.CharField(max_length=100, help_text="e.g., 'Our Mission', 'Who We Serve'")
    description = models.TextField()
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Mission Card"
        verbose_name_plural = "Mission Cards"

    def __str__(self):
        return self.label


class AboutFeatureCard(models.Model):
    """About Page 'What Sets Us Apart' feature card"""
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='feature_cards')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Feature Card"
        verbose_name_plural = "Feature Cards"

    def __str__(self):
        return self.title


class AboutValue(models.Model):
    """About Page value item"""
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='values')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Value"
        verbose_name_plural = "Values"

    def __str__(self):
        return self.title


class AboutTeamMember(models.Model):
    """About Page team member"""
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)
    avatar_alt = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.role}"


class ServicesPage(models.Model):
    """Services Page content"""
    # Hero Section
    badge = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    hero_image_1_url = models.URLField(max_length=500, blank=True)
    hero_image_1_alt = models.CharField(max_length=200, blank=True)
    hero_image_2_url = models.URLField(max_length=500, blank=True)
    hero_image_2_alt = models.CharField(max_length=200, blank=True)
    hero_image_3_url = models.URLField(max_length=500, blank=True)
    hero_image_3_alt = models.CharField(max_length=200, blank=True)
    hero_label = models.CharField(max_length=200, blank=True, help_text="Floating label text")
    
    # Full Marble Solutions
    solutions_title = models.CharField(max_length=200, blank=True)
    solutions_description = models.TextField(blank=True)
    
    # Process Section
    process_title = models.CharField(max_length=200, blank=True)
    process_description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Services Page"
        verbose_name_plural = "Services Page"

    def __str__(self):
        return "Services Page"


class ServicesPageService(models.Model):
    """Services Page individual service section"""
    services_page = models.ForeignKey(ServicesPage, on_delete=models.CASCADE, related_name='services')
    service_id = models.CharField(max_length=100, help_text="Anchor ID (e.g., 'kitchen-marble-work')")
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    image_url = models.URLField(max_length=500, blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    features_json = models.JSONField(default=list, blank=True, help_text="Array of feature strings")
    additional_text = models.TextField(blank=True)
    image_position = models.CharField(max_length=20, choices=[('left', 'Left'), ('right', 'Right')], default='right')
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Service Section"
        verbose_name_plural = "Service Sections"

    def __str__(self):
        return self.title


class ServicesPageProcessStep(models.Model):
    """Services Page process step"""
    services_page = models.ForeignKey(ServicesPage, on_delete=models.CASCADE, related_name='process_steps')
    number = models.CharField(max_length=10, help_text="e.g., '01', '02'")
    title = models.CharField(max_length=200)
    description = models.TextField()
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Process Step"
        verbose_name_plural = "Process Steps"

    def __str__(self):
        return f"{self.number} - {self.title}"


class PortfolioPage(models.Model):
    """Portfolio Page content"""
    # Hero Section
    hero_badge = models.CharField(max_length=200, blank=True, help_text="Badge text above hero title")
    title = models.CharField(max_length=200)
    description = models.TextField()
    hero_image_1_url = models.URLField(max_length=500, blank=True, help_text="First rotating hero image")
    hero_image_1_alt = models.CharField(max_length=200, blank=True)
    hero_image_2_url = models.URLField(max_length=500, blank=True, help_text="Second rotating hero image")
    hero_image_2_alt = models.CharField(max_length=200, blank=True)
    hero_image_3_url = models.URLField(max_length=500, blank=True, help_text="Third rotating hero image")
    hero_image_3_alt = models.CharField(max_length=200, blank=True)
    
    # Residential Designs
    residential_badge = models.CharField(max_length=200, blank=True, help_text="Badge text for residential section")
    residential_title = models.CharField(max_length=200, blank=True)
    residential_description = models.TextField(blank=True)
    residential_featured_image_url = models.URLField(max_length=500, blank=True)
    residential_featured_image_alt = models.CharField(max_length=200, blank=True)
    residential_featured_title = models.CharField(max_length=200, blank=True)
    residential_featured_description = models.TextField(blank=True)
    
    # Commercial Spaces
    commercial_badge = models.CharField(max_length=200, blank=True, help_text="Badge text for commercial section")
    commercial_title = models.CharField(max_length=200, blank=True)
    commercial_description = models.TextField(blank=True)
    commercial_featured_image_url = models.URLField(max_length=500, blank=True)
    commercial_featured_image_alt = models.CharField(max_length=200, blank=True)
    commercial_featured_title = models.CharField(max_length=200, blank=True)
    commercial_featured_description = models.TextField(blank=True)
    
    # CTA Section
    cta_title = models.CharField(max_length=200, blank=True)
    cta_description = models.TextField(blank=True)
    cta_primary_label = models.CharField(max_length=200, blank=True)
    cta_primary_href = models.CharField(max_length=200, default="/contact/")
    cta_secondary_label = models.CharField(max_length=200, blank=True)
    cta_secondary_href = models.CharField(max_length=200, default="/services/")

    class Meta:
        verbose_name = "Portfolio Page"
        verbose_name_plural = "Portfolio Page"

    def __str__(self):
        return "Portfolio Page"


class PortfolioPageCategory(models.Model):
    """Portfolio Page category card"""
    portfolio_page = models.ForeignKey(PortfolioPage, on_delete=models.CASCADE, related_name='categories')
    category_type = models.CharField(max_length=20, choices=[('residential', 'Residential'), ('commercial', 'Commercial')], default='residential')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Optional description for the category")
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    image_url = models.URLField(max_length=500, blank=True, help_text="Category image URL")
    image_alt = models.CharField(max_length=200, blank=True, help_text="Image alt text")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Portfolio Category"
        verbose_name_plural = "Portfolio Categories"

    def __str__(self):
        return f"{self.category_type} - {self.title}"


class FAQPage(models.Model):
    """FAQ Page content"""
    # Hero Section
    badge = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    hero_image_url = models.URLField(max_length=500, blank=True)
    hero_image_alt = models.CharField(max_length=200, blank=True)
    hero_label = models.CharField(max_length=200, blank=True)
    
    # Micro CTA Strip
    micro_cta_title = models.CharField(max_length=200, blank=True)
    micro_cta_description = models.TextField(blank=True)
    
    # Final Conversion Band
    final_cta_title = models.CharField(max_length=200, blank=True)
    final_cta_description = models.TextField(blank=True)
    final_cta_note_1 = models.CharField(max_length=200, blank=True)
    final_cta_note_2 = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "FAQ Page"
        verbose_name_plural = "FAQ Page"

    def __str__(self):
        return "FAQ Page"


class FAQPageSection(models.Model):
    """FAQ Page section (General, Pricing, Durability, Warranty)"""
    faq_page = models.ForeignKey(FAQPage, on_delete=models.CASCADE, related_name='sections')
    section_id = models.CharField(max_length=100, help_text="Anchor ID (e.g., 'faq-general')")
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "FAQ Section"
        verbose_name_plural = "FAQ Sections"

    def __str__(self):
        return self.title


class FAQPageQuestion(models.Model):
    """FAQ Page question item"""
    faq_section = models.ForeignKey(FAQPageSection, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "FAQ Question"
        verbose_name_plural = "FAQ Questions"

    def __str__(self):
        return self.question


class FAQPageTip(models.Model):
    """FAQ Page tip card (e.g., maintenance tips)"""
    faq_section = models.ForeignKey(FAQPageSection, on_delete=models.CASCADE, related_name='tips')
    title = models.CharField(max_length=200)
    description = models.TextField()
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "FAQ Tip"
        verbose_name_plural = "FAQ Tips"

    def __str__(self):
        return self.title


class ContactPage(models.Model):
    """Contact Page content"""
    # Hero Section
    badge = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    hero_feature_1_text = models.CharField(max_length=200, blank=True)
    hero_feature_2_text = models.CharField(max_length=200, blank=True)
    hero_background_image_url = models.URLField(max_length=500, blank=True)
    
    # Contact Details Section
    contact_details_title = models.CharField(max_length=200, blank=True)
    contact_details_description = models.TextField(blank=True)
    
    # Business Hours Section
    business_hours_title = models.CharField(max_length=200, blank=True)
    business_hours_description = models.TextField(blank=True)
    business_hours_json = models.JSONField(default=list, blank=True, help_text="Array of {day, hours} objects")

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Page"

    def __str__(self):
        return "Contact Page"
