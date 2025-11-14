from django.contrib import admin
from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Service, Services,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer
)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'public_id', 'width', 'height', 'format', 'bytes_size', 'is_active', 'created_at']
    list_filter = ['is_active', 'format', 'created_at']
    search_fields = ['title', 'public_id', 'tags_csv']
    readonly_fields = ['secure_url', 'web_url', 'thumb_url', 'bytes_size', 'width', 'height', 'format', 'created_at', 'updated_at']


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ['title', 'canonical']


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ['brand', 'logo_text']


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['headline', 'badge']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'badge']


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['value', 'label', 'sort_order']
    list_editable = ['sort_order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_open', 'sort_order']
    list_editable = ['sort_order', 'is_open']


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['heading']


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_order']
    list_editable = ['sort_order']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'sort_order']
    list_editable = ['sort_order']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'sort_order']
    list_editable = ['sort_order']


@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['heading', 'badge']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['label', 'text', 'info_type', 'sort_order']
    list_editable = ['sort_order']


@admin.register(ContactFormField)
class ContactFormFieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'label', 'field_type', 'required', 'span', 'sort_order']
    list_editable = ['sort_order', 'required']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['icon', 'href', 'sort_order']
    list_editable = ['sort_order']


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['logo_text', 'note']
