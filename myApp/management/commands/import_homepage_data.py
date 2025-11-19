"""
Management command to import homepage.json data into the database
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps

from myApp.models import (
    SEO, Navigation, Hero, About, Stat, Service, Services,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer,
    Promise, PromiseCard, FeaturedServices, FeaturedService, WhyTrust, WhyTrustFactor
)


class Command(BaseCommand):
    help = 'Import homepage.json data into the database'

    def handle(self, *args, **options):
        # Load JSON file
        json_path = Path(__file__).parent.parent.parent / 'content' / 'homepage.json'
        
        if not json_path.exists():
            self.stdout.write(self.style.ERROR('homepage.json not found!'))
            return
        
        with json_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.stdout.write(self.style.SUCCESS('Importing homepage data...'))
        
        # Import SEO
        seo_data = data.get('seo', {})
        seo, created = SEO.objects.get_or_create(pk=1, defaults={
            'title': seo_data.get('title', ''),
            'description': seo_data.get('description', ''),
            'canonical': seo_data.get('canonical', ''),
            'og_title': seo_data.get('og', {}).get('title', ''),
            'og_description': seo_data.get('og', {}).get('description', ''),
            'og_image': seo_data.get('og', {}).get('image', ''),
            'favicon': seo_data.get('favicon', ''),
            'preload_hero': seo_data.get('preload_hero', ''),
        })
        if not created:
            seo.title = seo_data.get('title', '')
            seo.description = seo_data.get('description', '')
            seo.canonical = seo_data.get('canonical', '')
            seo.og_title = seo_data.get('og', {}).get('title', '')
            seo.og_description = seo_data.get('og', {}).get('description', '')
            seo.og_image = seo_data.get('og', {}).get('image', '')
            seo.favicon = seo_data.get('favicon', '')
            seo.preload_hero = seo_data.get('preload_hero', '')
            seo.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ SEO imported'))
        
        # Import Navigation
        nav_data = data.get('nav', {})
        nav, created = Navigation.objects.get_or_create(pk=1, defaults={
            'logo_text': nav_data.get('logo_text', 'MM'),
            'brand': nav_data.get('brand', 'Madrid Marble'),
            'links_json': nav_data.get('links', []),
            'cta_label': nav_data.get('cta', {}).get('label', ''),
            'cta_href': nav_data.get('cta', {}).get('href', '#contact'),
        })
        if not created:
            nav.logo_text = nav_data.get('logo_text', 'MM')
            nav.brand = nav_data.get('brand', 'Madrid Marble')
            nav.links_json = nav_data.get('links', [])
            nav.cta_label = nav_data.get('cta', {}).get('label', '')
            nav.cta_href = nav_data.get('cta', {}).get('href', '#contact')
            nav.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Navigation imported'))
        
        # Import Hero
        hero_data = data.get('hero', {})
        hero, created = Hero.objects.get_or_create(pk=1, defaults={
            'badge': hero_data.get('badge', ''),
            'eyebrow': hero_data.get('eyebrow', ''),
            'headline': hero_data.get('headline', ''),
            'description': hero_data.get('description', ''),
            'image_url': hero_data.get('image', {}).get('url', ''),
            'image_alt': hero_data.get('image', {}).get('alt', ''),
            'primary_cta_label': hero_data.get('primary_cta', {}).get('label', ''),
            'primary_cta_href': hero_data.get('primary_cta', {}).get('href', '#contact'),
            'primary_cta_icon': hero_data.get('primary_cta', {}).get('icon', ''),
            'secondary_cta_label': hero_data.get('secondary_cta', {}).get('label', ''),
            'secondary_cta_href': hero_data.get('secondary_cta', {}).get('href', ''),
            'testimonial_quote': hero_data.get('testimonial', {}).get('quote', ''),
            'testimonial_name': hero_data.get('testimonial', {}).get('name', ''),
            'testimonial_meta': hero_data.get('testimonial', {}).get('meta', ''),
            'testimonial_stars': hero_data.get('testimonial', {}).get('stars', 5),
            'stats_json': hero_data.get('stats', []),
        })
        if not created:
            hero.badge = hero_data.get('badge', '')
            hero.eyebrow = hero_data.get('eyebrow', '')
            hero.headline = hero_data.get('headline', '')
            hero.description = hero_data.get('description', '')
            hero.image_url = hero_data.get('image', {}).get('url', '')
            hero.image_alt = hero_data.get('image', {}).get('alt', '')
            hero.primary_cta_label = hero_data.get('primary_cta', {}).get('label', '')
            hero.primary_cta_href = hero_data.get('primary_cta', {}).get('href', '#contact')
            hero.primary_cta_icon = hero_data.get('primary_cta', {}).get('icon', '')
            hero.secondary_cta_label = hero_data.get('secondary_cta', {}).get('label', '')
            hero.secondary_cta_href = hero_data.get('secondary_cta', {}).get('href', '')
            hero.testimonial_quote = hero_data.get('testimonial', {}).get('quote', '')
            hero.testimonial_name = hero_data.get('testimonial', {}).get('name', '')
            hero.testimonial_meta = hero_data.get('testimonial', {}).get('meta', '')
            hero.testimonial_stars = hero_data.get('testimonial', {}).get('stars', 5)
            hero.stats_json = hero_data.get('stats', [])
            hero.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Hero imported'))
        
        # Import About
        about_data = data.get('about', {})
        about, created = About.objects.get_or_create(pk=1, defaults={
            'badge': about_data.get('badge', ''),
            'title': about_data.get('title', ''),
            'copy_json': about_data.get('copy', []),
            'gallery_json': about_data.get('gallery', []),
        })
        if not created:
            about.badge = about_data.get('badge', '')
            about.title = about_data.get('title', '')
            about.copy_json = about_data.get('copy', [])
            about.gallery_json = about_data.get('gallery', [])
            about.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ About imported'))
        
        # Import Stats
        stats_data = data.get('stats', [])
        Stat.objects.all().delete()
        for idx, stat_data in enumerate(stats_data):
            Stat.objects.create(
                value=stat_data.get('value', ''),
                label=stat_data.get('label', ''),
                description=stat_data.get('description', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(stats_data)} Stats imported'))
        
        # Import Promise Section
        promise_data = data.get('promise', {})
        promise, created = Promise.objects.get_or_create(pk=1, defaults={
            'title': promise_data.get('title', 'Our Promise'),
            'main_statement': promise_data.get('main_statement', ''),
            'substatement': promise_data.get('substatement', ''),
            'closing_statement': promise_data.get('closing_statement', ''),
        })
        if not created:
            promise.title = promise_data.get('title', 'Our Promise')
            promise.main_statement = promise_data.get('main_statement', '')
            promise.substatement = promise_data.get('substatement', '')
            promise.closing_statement = promise_data.get('closing_statement', '')
            promise.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Promise Section imported'))
        
        # Import Promise Cards
        promise_cards_data = promise_data.get('cards', [])
        PromiseCard.objects.all().delete()
        for idx, card_data in enumerate(promise_cards_data):
            PromiseCard.objects.create(
                title=card_data.get('title', ''),
                description=card_data.get('description', ''),
                icon=card_data.get('icon', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(promise_cards_data)} Promise Cards imported'))
        
        # Import Featured Services Section
        featured_services_data = data.get('featured_services', {})
        featured_services_section, created = FeaturedServices.objects.get_or_create(pk=1, defaults={
            'title': featured_services_data.get('title', 'Featured Services'),
            'description': featured_services_data.get('description', ''),
        })
        if not created:
            featured_services_section.title = featured_services_data.get('title', 'Featured Services')
            featured_services_section.description = featured_services_data.get('description', '')
            featured_services_section.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Featured Services Section imported'))
        
        # Import Featured Services
        featured_services_items = featured_services_data.get('items', [])
        FeaturedService.objects.all().delete()
        for idx, service_data in enumerate(featured_services_items):
            FeaturedService.objects.create(
                title=service_data.get('title', ''),
                description=service_data.get('description', ''),
                icon=service_data.get('icon', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(featured_services_items)} Featured Services imported'))
        
        # Import Services Section
        services_data = data.get('services', {})
        services_section, created = Services.objects.get_or_create(pk=1, defaults={
            'title': services_data.get('title', ''),
            'description': services_data.get('description', ''),
            'image_url': services_data.get('image', {}).get('url', ''),
            'image_alt': services_data.get('image', {}).get('alt', ''),
        })
        if not created:
            services_section.title = services_data.get('title', '')
            services_section.description = services_data.get('description', '')
            services_section.image_url = services_data.get('image', {}).get('url', '')
            services_section.image_alt = services_data.get('image', {}).get('alt', '')
            services_section.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Services Section imported'))
        
        # Import Services
        services_items = services_data.get('items', [])
        Service.objects.all().delete()
        for idx, service_data in enumerate(services_items):
            Service.objects.create(
                title=service_data.get('title', ''),
                description=service_data.get('description', ''),
                icon=service_data.get('icon', ''),
                is_open=service_data.get('open', False),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(services_items)} Services imported'))
        
        # Import Why Trust Section
        why_trust_data = data.get('why_trust', {})
        why_trust, created = WhyTrust.objects.get_or_create(pk=1, defaults={
            'title': why_trust_data.get('title', 'Why Clients Trust Madrid Marble'),
            'subtitle': why_trust_data.get('subtitle', ''),
        })
        if not created:
            why_trust.title = why_trust_data.get('title', 'Why Clients Trust Madrid Marble')
            why_trust.subtitle = why_trust_data.get('subtitle', '')
            why_trust.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Why Trust Section imported'))
        
        # Import Why Trust Factors
        why_trust_factors_data = why_trust_data.get('factors', [])
        WhyTrustFactor.objects.all().delete()
        for idx, factor_data in enumerate(why_trust_factors_data):
            WhyTrustFactor.objects.create(
                title=factor_data.get('title', ''),
                description=factor_data.get('description', ''),
                icon=factor_data.get('icon', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(why_trust_factors_data)} Why Trust Factors imported'))
        
        # Import Portfolio
        portfolio_data = data.get('portfolio', {})
        portfolio, created = Portfolio.objects.get_or_create(pk=1, defaults={
            'heading': portfolio_data.get('heading', ''),
            'description': portfolio_data.get('description', ''),
            'feature_image_url': portfolio_data.get('feature', {}).get('image', {}).get('url', ''),
            'feature_image_alt': portfolio_data.get('feature', {}).get('image', {}).get('alt', ''),
            'feature_title': portfolio_data.get('feature', {}).get('title', ''),
            'feature_description': portfolio_data.get('feature', {}).get('description', ''),
            'feature_tags_json': portfolio_data.get('feature', {}).get('tags', []),
            'feature_testimonial_quote': portfolio_data.get('feature', {}).get('testimonial', {}).get('quote', ''),
            'feature_testimonial_author': portfolio_data.get('feature', {}).get('testimonial', {}).get('author', ''),
            'feature_cta_label': portfolio_data.get('feature', {}).get('cta', {}).get('label', ''),
            'feature_cta_href': portfolio_data.get('feature', {}).get('cta', {}).get('href', '#contact'),
            'feature_cta_icon': portfolio_data.get('feature', {}).get('cta', {}).get('icon', ''),
        })
        if not created:
            portfolio.heading = portfolio_data.get('heading', '')
            portfolio.description = portfolio_data.get('description', '')
            portfolio.feature_image_url = portfolio_data.get('feature', {}).get('image', {}).get('url', '')
            portfolio.feature_image_alt = portfolio_data.get('feature', {}).get('image', {}).get('alt', '')
            portfolio.feature_title = portfolio_data.get('feature', {}).get('title', '')
            portfolio.feature_description = portfolio_data.get('feature', {}).get('description', '')
            portfolio.feature_tags_json = portfolio_data.get('feature', {}).get('tags', [])
            portfolio.feature_testimonial_quote = portfolio_data.get('feature', {}).get('testimonial', {}).get('quote', '')
            portfolio.feature_testimonial_author = portfolio_data.get('feature', {}).get('testimonial', {}).get('author', '')
            portfolio.feature_cta_label = portfolio_data.get('feature', {}).get('cta', {}).get('label', '')
            portfolio.feature_cta_href = portfolio_data.get('feature', {}).get('cta', {}).get('href', '#contact')
            portfolio.feature_cta_icon = portfolio_data.get('feature', {}).get('cta', {}).get('icon', '')
            portfolio.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Portfolio Section imported'))
        
        # Import Portfolio Projects
        portfolio_projects = portfolio_data.get('projects', [])
        PortfolioProject.objects.all().delete()
        for idx, project_data in enumerate(portfolio_projects):
            PortfolioProject.objects.create(
                image_url=project_data.get('image', {}).get('url', ''),
                image_alt=project_data.get('image', {}).get('alt', ''),
                title=project_data.get('title', ''),
                description=project_data.get('description', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(portfolio_projects)} Portfolio Projects imported'))
        
        # Import Testimonials
        testimonials_data = data.get('testimonials', [])
        Testimonial.objects.all().delete()
        for idx, testimonial_data in enumerate(testimonials_data):
            Testimonial.objects.create(
                quote=testimonial_data.get('quote', ''),
                name=testimonial_data.get('name', ''),
                role=testimonial_data.get('role', ''),
                avatar=testimonial_data.get('avatar', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(testimonials_data)} Testimonials imported'))
        
        # Import FAQ Section
        faq_data = data.get('faq', {})
        faq_section, created = FAQSection.objects.get_or_create(pk=1, defaults={
            'title': faq_data.get('title', ''),
            'description': faq_data.get('description', ''),
            'cta_label': faq_data.get('cta', {}).get('label', ''),
            'cta_href': faq_data.get('cta', {}).get('href', '#contact'),
            'cta_icon': faq_data.get('cta', {}).get('icon', ''),
        })
        if not created:
            faq_section.title = faq_data.get('title', '')
            faq_section.description = faq_data.get('description', '')
            faq_section.cta_label = faq_data.get('cta', {}).get('label', '')
            faq_section.cta_href = faq_data.get('cta', {}).get('href', '#contact')
            faq_section.cta_icon = faq_data.get('cta', {}).get('icon', '')
            faq_section.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ FAQ Section imported'))
        
        # Import FAQs
        faqs_items = faq_data.get('items', [])
        FAQ.objects.all().delete()
        for idx, faq_item in enumerate(faqs_items):
            FAQ.objects.create(
                question=faq_item.get('question', ''),
                answer=faq_item.get('answer', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(faqs_items)} FAQs imported'))
        
        # Import Contact
        contact_data = data.get('contact', {})
        contact, created = Contact.objects.get_or_create(pk=1, defaults={
            'badge': contact_data.get('badge', 'CONTACT'),
            'heading': contact_data.get('heading', ''),
            'description': contact_data.get('description', ''),
            'intro_text': contact_data.get('intro_text', ''),
            'background_image': contact_data.get('background_image', ''),
            'socials_label': contact_data.get('socials', {}).get('label', 'FOLLOW MADRID MARBLE'),
            'form_submit_label': contact_data.get('form', {}).get('submit', {}).get('label', 'Submit inquiry'),
            'form_disclaimer': contact_data.get('form', {}).get('disclaimer', ''),
        })
        if not created:
            contact.badge = contact_data.get('badge', 'CONTACT')
            contact.heading = contact_data.get('heading', '')
            contact.description = contact_data.get('description', '')
            contact.intro_text = contact_data.get('intro_text', '')
            contact.background_image = contact_data.get('background_image', '')
            contact.socials_label = contact_data.get('socials', {}).get('label', 'FOLLOW MADRID MARBLE')
            contact.form_submit_label = contact_data.get('form', {}).get('submit', {}).get('label', 'Submit inquiry')
            contact.form_disclaimer = contact_data.get('form', {}).get('disclaimer', '')
            contact.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Contact Section imported'))
        
        # Import Contact Info
        contact_info_data = contact_data.get('info', [])
        ContactInfo.objects.all().delete()
        for idx, info_data in enumerate(contact_info_data):
            ContactInfo.objects.create(
                label=info_data.get('label', ''),
                text=info_data.get('text', ''),
                href=info_data.get('href', ''),
                info_type=info_data.get('type', 'address'),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(contact_info_data)} Contact Info items imported'))
        
        # Import Contact Form Fields
        contact_form_fields = contact_data.get('form', {}).get('fields', [])
        ContactFormField.objects.all().delete()
        for idx, field_data in enumerate(contact_form_fields):
            ContactFormField.objects.create(
                contact=contact,
                name=field_data.get('name', ''),
                label=field_data.get('label', ''),
                field_type=field_data.get('type', 'text'),
                placeholder=field_data.get('placeholder', ''),
                span=field_data.get('span', 1),
                rows=field_data.get('rows', 5),
                required=field_data.get('required', True),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(contact_form_fields)} Contact Form Fields imported'))
        
        # Import Social Links
        social_links_data = contact_data.get('socials', {}).get('links', [])
        SocialLink.objects.all().delete()
        for idx, link_data in enumerate(social_links_data):
            SocialLink.objects.create(
                icon=link_data.get('icon', ''),
                href=link_data.get('href', ''),
                sort_order=idx
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(social_links_data)} Social Links imported'))
        
        # Import Footer
        footer_data = data.get('footer', {})
        footer, created = Footer.objects.get_or_create(pk=1, defaults={
            'logo_text': footer_data.get('logo_text', 'MM'),
            'note': footer_data.get('note', 'Madrid Marble. All rights reserved.'),
            'links_json': footer_data.get('links', []),
        })
        if not created:
            footer.logo_text = footer_data.get('logo_text', 'MM')
            footer.note = footer_data.get('note', 'Madrid Marble. All rights reserved.')
            footer.links_json = footer_data.get('links', [])
            footer.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Footer imported'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All data imported successfully!'))
        self.stdout.write(self.style.SUCCESS('\n📝 Note: Make sure your homepage.json includes the new sections:'))
        self.stdout.write(self.style.SUCCESS('   - promise (with cards array)'))
        self.stdout.write(self.style.SUCCESS('   - featured_services (with items array)'))
        self.stdout.write(self.style.SUCCESS('   - why_trust (with factors array)'))
        self.stdout.write(self.style.SUCCESS('   - hero.eyebrow and hero.stats (array)'))







