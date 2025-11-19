"""
Management command to export all database data to JSON file for backup/seed
This creates a complete backup of all content before making changes
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from myApp.models import (
    SEO, Navigation, Hero, About, Stat, Service, Services,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer,
    Promise, PromiseCard, FeaturedServices, FeaturedService, WhyTrust, WhyTrustFactor
)


class Command(BaseCommand):
    help = 'Export all database data to JSON file for backup/seed'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='backup_data.json',
            help='Output filename (default: backup_data.json)'
        )

    def handle(self, *args, **options):
        output_file = Path(__file__).parent.parent.parent / options['output']
        
        self.stdout.write(self.style.SUCCESS('Exporting all data...'))
        
        # Collect all data
        data = {}
        
        # SEO
        seo = SEO.objects.first()
        if seo:
            data['seo'] = {
                'title': seo.title,
                'description': seo.description,
                'canonical': seo.canonical,
                'og_title': seo.og_title,
                'og_description': seo.og_description,
                'og_image': seo.og_image,
                'favicon': seo.favicon,
                'preload_hero': seo.preload_hero,
            }
        
        # Navigation
        nav = Navigation.objects.first()
        if nav:
            data['nav'] = {
                'logo_text': nav.logo_text,
                'logo_image_url': nav.logo_image_url,
                'brand': nav.brand,
                'links_json': nav.links_json,
                'cta_label': nav.cta_label,
                'cta_href': nav.cta_href,
            }
        
        # Hero
        hero = Hero.objects.first()
        if hero:
            data['hero'] = {
                'badge': hero.badge,
                'eyebrow': hero.eyebrow,
                'headline': hero.headline,
                'description': hero.description,
                'image_url': hero.image_url,
                'image_alt': hero.image_alt,
                'primary_cta_label': hero.primary_cta_label,
                'primary_cta_href': hero.primary_cta_href,
                'primary_cta_icon': hero.primary_cta_icon,
                'secondary_cta_label': hero.secondary_cta_label,
                'secondary_cta_href': hero.secondary_cta_href,
                'testimonial_quote': hero.testimonial_quote,
                'testimonial_name': hero.testimonial_name,
                'testimonial_meta': hero.testimonial_meta,
                'testimonial_stars': hero.testimonial_stars,
                'stats': hero.stats_json,
            }
        
        # About (Landing Page Section)
        about = About.objects.first()
        if about:
            data['about'] = {
                'badge': about.badge,
                'title': about.title,
                'copy_json': about.copy_json,
                'gallery_json': about.gallery_json,
            }
        
        # Stats
        stats = Stat.objects.all().order_by('sort_order')
        data['stats'] = [
            {
                'value': stat.value,
                'label': stat.label,
                'description': stat.description,
                'sort_order': stat.sort_order,
            }
            for stat in stats
        ]
        
        # Promise Section
        promise = Promise.objects.first()
        if promise:
            data['promise'] = {
                'title': promise.title,
                'main_statement': promise.main_statement,
                'substatement': promise.substatement,
                'closing_statement': promise.closing_statement,
                'cards': [
                    {
                        'title': card.title,
                        'description': card.description,
                        'icon': card.icon,
                        'sort_order': card.sort_order,
                    }
                    for card in PromiseCard.objects.all().order_by('sort_order')
                ]
            }
        
        # Featured Services
        featured_services_section = FeaturedServices.objects.first()
        if featured_services_section:
            data['featured_services'] = {
                'title': featured_services_section.title,
                'description': featured_services_section.description,
                'items': [
                    {
                        'title': service.title,
                        'description': service.description,
                        'icon': service.icon,
                        'sort_order': service.sort_order,
                    }
                    for service in FeaturedService.objects.all().order_by('sort_order')
                ]
            }
        
        # Services Section
        services_section = Services.objects.first()
        if services_section:
            data['services'] = {
                'title': services_section.title,
                'description': services_section.description,
                'image_url': services_section.image_url,
                'image_alt': services_section.image_alt,
                'items': [
                    {
                        'title': service.title,
                        'description': service.description,
                        'icon': service.icon,
                        'is_open': service.is_open,
                        'sort_order': service.sort_order,
                    }
                    for service in Service.objects.all().order_by('sort_order')
                ]
            }
        
        # Why Trust
        why_trust = WhyTrust.objects.first()
        if why_trust:
            data['why_trust'] = {
                'title': why_trust.title,
                'subtitle': why_trust.subtitle,
                'factors': [
                    {
                        'title': factor.title,
                        'description': factor.description,
                        'icon': factor.icon,
                        'sort_order': factor.sort_order,
                    }
                    for factor in WhyTrustFactor.objects.all().order_by('sort_order')
                ]
            }
        
        # Portfolio
        portfolio = Portfolio.objects.first()
        if portfolio:
            data['portfolio'] = {
                'heading': portfolio.heading,
                'description': portfolio.description,
                'feature_image_url': portfolio.feature_image_url,
                'feature_image_alt': portfolio.feature_image_alt,
                'feature_title': portfolio.feature_title,
                'feature_description': portfolio.feature_description,
                'feature_tags_json': portfolio.feature_tags_json,
                'feature_testimonial_quote': portfolio.feature_testimonial_quote,
                'feature_testimonial_author': portfolio.feature_testimonial_author,
                'feature_cta_label': portfolio.feature_cta_label,
                'feature_cta_href': portfolio.feature_cta_href,
                'feature_cta_icon': portfolio.feature_cta_icon,
                'projects': [
                    {
                        'image_url': project.image_url,
                        'image_alt': project.image_alt,
                        'title': project.title,
                        'description': project.description,
                        'sort_order': project.sort_order,
                        'is_active': project.is_active,
                    }
                    for project in PortfolioProject.objects.all().order_by('sort_order')
                ]
            }
        
        # Testimonials
        testimonials = Testimonial.objects.all().order_by('sort_order')
        data['testimonials'] = [
            {
                'quote': testimonial.quote,
                'name': testimonial.name,
                'role': testimonial.role,
                'avatar': testimonial.avatar,
                'sort_order': testimonial.sort_order,
            }
            for testimonial in testimonials
        ]
        
        # FAQ Section
        faq_section = FAQSection.objects.first()
        if faq_section:
            data['faq'] = {
                'title': faq_section.title,
                'description': faq_section.description,
                'cta_label': faq_section.cta_label,
                'cta_href': faq_section.cta_href,
                'cta_icon': faq_section.cta_icon,
                'items': [
                    {
                        'question': faq.question,
                        'answer': faq.answer,
                        'sort_order': faq.sort_order,
                    }
                    for faq in FAQ.objects.all().order_by('sort_order')
                ]
            }
        
        # Contact
        contact = Contact.objects.first()
        if contact:
            data['contact'] = {
                'badge': contact.badge,
                'heading': contact.heading,
                'description': contact.description,
                'intro_text': contact.intro_text,
                'background_image': contact.background_image,
                'socials_label': contact.socials_label,
                'form_submit_label': contact.form_submit_label,
                'form_disclaimer': contact.form_disclaimer,
                'info': [
                    {
                        'label': info.label,
                        'text': info.text,
                        'href': info.href,
                        'type': info.info_type,
                        'sort_order': info.sort_order,
                    }
                    for info in ContactInfo.objects.all().order_by('sort_order')
                ],
                'form': {
                    'fields': [
                        {
                            'name': field.name,
                            'label': field.label,
                            'type': field.field_type,
                            'placeholder': field.placeholder,
                            'span': field.span,
                            'rows': field.rows,
                            'required': field.required,
                            'sort_order': field.sort_order,
                        }
                        for field in ContactFormField.objects.all().order_by('sort_order')
                    ],
                    'submit': {
                        'label': contact.form_submit_label,
                    },
                    'disclaimer': contact.form_disclaimer,
                },
                'socials': {
                    'label': contact.socials_label,
                    'links': [
                        {
                            'icon': link.icon,
                            'href': link.href,
                            'sort_order': link.sort_order,
                        }
                        for link in SocialLink.objects.all().order_by('sort_order')
                    ]
                }
            }
        
        # Footer
        footer = Footer.objects.first()
        if footer:
            data['footer'] = {
                'logo_text': footer.logo_text,
                'note': footer.note,
                'links_json': footer.links_json,
            }
        
        # Write to file
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ All data exported successfully to {output_file.name}!'))
        self.stdout.write(self.style.SUCCESS(f'📁 Location: {output_file.absolute()}'))
        self.stdout.write(self.style.SUCCESS(f'\n💾 This file can be used to restore data using: python manage.py import_homepage_data'))

