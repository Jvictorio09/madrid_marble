"""
Management command to populate image URLs from MediaAsset database
or extract all available image URLs for use throughout the website.

Usage:
    python manage.py populate_image_urls --list          # List all image URLs
    python manage.py populate_image_urls --populate      # Auto-populate empty fields only
    python manage.py populate_image_urls --replace-all   # Replace ALL URLs (including existing ones)
    python manage.py populate_image_urls --report        # Generate detailed report
    python manage.py populate_image_urls --replace-all --dry-run  # Preview changes
"""

from django.core.management.base import BaseCommand
from django.db import models
from myApp.models import (
    MediaAsset, Navigation, Hero, About, Services, Portfolio, PortfolioProject,
    AboutPage, ServicesPage, ServicesPageService, PortfolioPage, FAQPage, ContactPage
)
import random


class Command(BaseCommand):
    help = 'Populate image URLs from MediaAsset database or list all available URLs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all image URLs available in the database',
        )
        parser.add_argument(
            '--populate',
            action='store_true',
            help='Auto-populate empty image URL fields with random MediaAsset URLs',
        )
        parser.add_argument(
            '--replace-all',
            action='store_true',
            help='Replace ALL image URLs (including existing ones) with MediaAsset URLs from gallery',
        )
        parser.add_argument(
            '--report',
            action='store_true',
            help='Generate a detailed report of all image fields and their status',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually making changes',
        )

    def handle(self, *args, **options):
        # Get all MediaAsset URLs
        media_assets = MediaAsset.objects.filter(is_active=True)
        asset_urls = list(media_assets.values_list('web_url', flat=True))
        
        if not asset_urls:
            self.stdout.write(self.style.WARNING(
                'No active MediaAsset URLs found in database. Upload images first via the dashboard gallery.'
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            f'Found {len(asset_urls)} active image URLs in MediaAsset database'
        ))

        if options['list']:
            self.list_urls(asset_urls)
        elif options['populate']:
            self.populate_urls(asset_urls, dry_run=options['dry_run'], replace_all=False)
        elif options['replace_all']:
            self.populate_urls(asset_urls, dry_run=options['dry_run'], replace_all=True)
        elif options['report']:
            self.generate_report(asset_urls)
        else:
            self.stdout.write(self.style.WARNING(
                'Please specify --list, --populate, --replace-all, or --report'
            ))

    def list_urls(self, asset_urls):
        """List all available image URLs"""
        self.stdout.write(self.style.SUCCESS('\n=== Available Image URLs ===\n'))
        for i, url in enumerate(asset_urls, 1):
            self.stdout.write(f'{i}. {url}')

    def populate_urls(self, asset_urls, dry_run=False, replace_all=False):
        """Populate image URL fields with MediaAsset URLs"""
        if not asset_urls:
            self.stdout.write(self.style.ERROR('No URLs available to populate'))
            return

        changes = []
        url_index = 0  # Cycle through URLs sequentially
        
        # Navigation logo
        nav = Navigation.objects.first()
        if nav:
            if replace_all or not nav.logo_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = nav.logo_image_url if nav.logo_image_url else 'EMPTY'
                if not dry_run:
                    nav.logo_image_url = url
                    nav.save()
                changes.append(('Navigation', 'logo_image_url', old_url, url))

        # Hero image
        hero = Hero.objects.first()
        if hero:
            if replace_all or not hero.image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = hero.image_url if hero.image_url else 'EMPTY'
                if not dry_run:
                    hero.image_url = url
                    hero.save()
                changes.append(('Hero', 'image_url', old_url, url))

        # About section
        about = About.objects.first()
        if about:
            # Check gallery_json - we'll skip this as it's JSON
            pass

        # Services section
        services = Services.objects.first()
        if services:
            if replace_all or not services.image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = services.image_url if services.image_url else 'EMPTY'
                if not dry_run:
                    services.image_url = url
                    services.save()
                changes.append(('Services', 'image_url', old_url, url))

        # Portfolio section
        portfolio = Portfolio.objects.first()
        if portfolio:
            if replace_all or not portfolio.feature_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = portfolio.feature_image_url if portfolio.feature_image_url else 'EMPTY'
                if not dry_run:
                    portfolio.feature_image_url = url
                    portfolio.save()
                changes.append(('Portfolio', 'feature_image_url', old_url, url))

        # Portfolio Projects
        if replace_all:
            projects = PortfolioProject.objects.filter(is_active=True)
        else:
            projects = PortfolioProject.objects.filter(image_url__isnull=True) | PortfolioProject.objects.filter(image_url='')
        
        for project in projects:
            if replace_all or not project.image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = project.image_url if project.image_url else 'EMPTY'
                if not dry_run:
                    project.image_url = url
                    project.save()
                changes.append((f'PortfolioProject #{project.id}', 'image_url', old_url, url))

        # About Page
        about_page = AboutPage.objects.first()
        if about_page:
            if replace_all or not about_page.hero_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = about_page.hero_image_url if about_page.hero_image_url else 'EMPTY'
                if not dry_run:
                    about_page.hero_image_url = url
                    about_page.save()
                changes.append(('AboutPage', 'hero_image_url', old_url, url))
            if replace_all or not about_page.workshop_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = about_page.workshop_image_url if about_page.workshop_image_url else 'EMPTY'
                if not dry_run:
                    about_page.workshop_image_url = url
                    about_page.save()
                changes.append(('AboutPage', 'workshop_image_url', old_url, url))

        # Services Page
        services_page = ServicesPage.objects.first()
        if services_page:
            if replace_all or not services_page.hero_image_1_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = services_page.hero_image_1_url if services_page.hero_image_1_url else 'EMPTY'
                if not dry_run:
                    services_page.hero_image_1_url = url
                    services_page.save()
                changes.append(('ServicesPage', 'hero_image_1_url', old_url, url))
            if replace_all or not services_page.hero_image_2_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = services_page.hero_image_2_url if services_page.hero_image_2_url else 'EMPTY'
                if not dry_run:
                    services_page.hero_image_2_url = url
                    services_page.save()
                changes.append(('ServicesPage', 'hero_image_2_url', old_url, url))
            if replace_all or not services_page.hero_image_3_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = services_page.hero_image_3_url if services_page.hero_image_3_url else 'EMPTY'
                if not dry_run:
                    services_page.hero_image_3_url = url
                    services_page.save()
                changes.append(('ServicesPage', 'hero_image_3_url', old_url, url))

        # Services Page Services
        if services_page:
            services_list = services_page.services.all()
            for service in services_list:
                if replace_all or not service.image_url:
                    url = asset_urls[url_index % len(asset_urls)]
                    url_index += 1
                    old_url = service.image_url if service.image_url else 'EMPTY'
                    if not dry_run:
                        service.image_url = url
                        service.save()
                    changes.append((f'ServicesPageService #{service.id}', 'image_url', old_url, url))

        # Portfolio Page
        portfolio_page = PortfolioPage.objects.first()
        if portfolio_page:
            if replace_all or not portfolio_page.hero_image_1_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = portfolio_page.hero_image_1_url if portfolio_page.hero_image_1_url else 'EMPTY'
                if not dry_run:
                    portfolio_page.hero_image_1_url = url
                    portfolio_page.save()
                changes.append(('PortfolioPage', 'hero_image_1_url', old_url, url))
            if replace_all or not portfolio_page.hero_image_2_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = portfolio_page.hero_image_2_url if portfolio_page.hero_image_2_url else 'EMPTY'
                if not dry_run:
                    portfolio_page.hero_image_2_url = url
                    portfolio_page.save()
                changes.append(('PortfolioPage', 'hero_image_2_url', old_url, url))
            if replace_all or not portfolio_page.hero_image_3_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = portfolio_page.hero_image_3_url if portfolio_page.hero_image_3_url else 'EMPTY'
                if not dry_run:
                    portfolio_page.hero_image_3_url = url
                    portfolio_page.save()
                changes.append(('PortfolioPage', 'hero_image_3_url', old_url, url))
            if replace_all or not portfolio_page.residential_featured_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = portfolio_page.residential_featured_image_url if portfolio_page.residential_featured_image_url else 'EMPTY'
                if not dry_run:
                    portfolio_page.residential_featured_image_url = url
                    portfolio_page.save()
                changes.append(('PortfolioPage', 'residential_featured_image_url', old_url, url))
            if replace_all or not portfolio_page.commercial_featured_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = portfolio_page.commercial_featured_image_url if portfolio_page.commercial_featured_image_url else 'EMPTY'
                if not dry_run:
                    portfolio_page.commercial_featured_image_url = url
                    portfolio_page.save()
                changes.append(('PortfolioPage', 'commercial_featured_image_url', old_url, url))

        # FAQ Page
        faq_page = FAQPage.objects.first()
        if faq_page:
            if replace_all or not faq_page.hero_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = faq_page.hero_image_url if faq_page.hero_image_url else 'EMPTY'
                if not dry_run:
                    faq_page.hero_image_url = url
                    faq_page.save()
                changes.append(('FAQPage', 'hero_image_url', old_url, url))

        # Contact Page
        contact_page = ContactPage.objects.first()
        if contact_page:
            if replace_all or not contact_page.hero_background_image_url:
                url = asset_urls[url_index % len(asset_urls)]
                url_index += 1
                old_url = contact_page.hero_background_image_url if contact_page.hero_background_image_url else 'EMPTY'
                if not dry_run:
                    contact_page.hero_background_image_url = url
                    contact_page.save()
                changes.append(('ContactPage', 'hero_background_image_url', old_url, url))

        # Report results
        if changes:
            action = "Would replace" if replace_all else "Would populate"
            if not dry_run:
                action = "Replaced" if replace_all else "Populated"
            
            self.stdout.write(self.style.SUCCESS(f'\n=== {action} {len(changes)} image URLs ===\n'))
            for item in changes:
                if len(item) == 4:  # New format with old_url
                    model_name, field_name, old_url, new_url = item
                    status = '[DRY RUN]' if dry_run else '[UPDATED]'
                    old_display = old_url[:50] + '...' if len(old_url) > 50 else old_url
                    new_display = new_url[:50] + '...' if len(new_url) > 50 else new_url
                    self.stdout.write(f'{status} {model_name}.{field_name}:')
                    self.stdout.write(f'    OLD: {old_display}')
                    self.stdout.write(f'    NEW: {new_display}\n')
                else:  # Old format (backward compatibility)
                    model_name, field_name, url = item
                    status = '[DRY RUN]' if dry_run else '[UPDATED]'
                    self.stdout.write(f'{status} {model_name}.{field_name}: {url[:80]}...')
            
            if dry_run:
                mode = "--replace-all" if replace_all else "--populate"
                self.stdout.write(self.style.WARNING(f'\nRun without --dry-run to apply changes: python manage.py populate_image_urls {mode}'))
            else:
                self.stdout.write(self.style.SUCCESS('\nAll changes applied successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('No image fields found to update.'))

    def generate_report(self, asset_urls):
        """Generate a detailed report of all image fields"""
        self.stdout.write(self.style.SUCCESS('\n=== Image URL Status Report ===\n'))
        
        report = []
        
        # Navigation
        nav = Navigation.objects.first()
        if nav:
            report.append(('Navigation', 'logo_image_url', nav.logo_image_url, bool(nav.logo_image_url)))
        
        # Hero
        hero = Hero.objects.first()
        if hero:
            report.append(('Hero', 'image_url', hero.image_url, bool(hero.image_url)))
        
        # Services
        services = Services.objects.first()
        if services:
            report.append(('Services', 'image_url', services.image_url, bool(services.image_url)))
        
        # Portfolio
        portfolio = Portfolio.objects.first()
        if portfolio:
            report.append(('Portfolio', 'feature_image_url', portfolio.feature_image_url, bool(portfolio.feature_image_url)))
        
        # Portfolio Projects
        projects = PortfolioProject.objects.all()
        for project in projects[:5]:  # Show first 5
            report.append((f'PortfolioProject #{project.id}', 'image_url', project.image_url, bool(project.image_url)))
        
        # About Page
        about_page = AboutPage.objects.first()
        if about_page:
            report.append(('AboutPage', 'hero_image_url', about_page.hero_image_url, bool(about_page.hero_image_url)))
            report.append(('AboutPage', 'workshop_image_url', about_page.workshop_image_url, bool(about_page.workshop_image_url)))
        
        # Services Page
        services_page = ServicesPage.objects.first()
        if services_page:
            report.append(('ServicesPage', 'hero_image_1_url', services_page.hero_image_1_url, bool(services_page.hero_image_1_url)))
            report.append(('ServicesPage', 'hero_image_2_url', services_page.hero_image_2_url, bool(services_page.hero_image_2_url)))
            report.append(('ServicesPage', 'hero_image_3_url', services_page.hero_image_3_url, bool(services_page.hero_image_3_url)))
        
        # Portfolio Page
        portfolio_page = PortfolioPage.objects.first()
        if portfolio_page:
            report.append(('PortfolioPage', 'hero_image_1_url', portfolio_page.hero_image_1_url, bool(portfolio_page.hero_image_1_url)))
            report.append(('PortfolioPage', 'hero_image_2_url', portfolio_page.hero_image_2_url, bool(portfolio_page.hero_image_2_url)))
            report.append(('PortfolioPage', 'hero_image_3_url', portfolio_page.hero_image_3_url, bool(portfolio_page.hero_image_3_url)))
            report.append(('PortfolioPage', 'residential_featured_image_url', portfolio_page.residential_featured_image_url, bool(portfolio_page.residential_featured_image_url)))
            report.append(('PortfolioPage', 'commercial_featured_image_url', portfolio_page.commercial_featured_image_url, bool(portfolio_page.commercial_featured_image_url)))
        
        # FAQ Page
        faq_page = FAQPage.objects.first()
        if faq_page:
            report.append(('FAQPage', 'hero_image_url', faq_page.hero_image_url, bool(faq_page.hero_image_url)))
        
        # Contact Page
        contact_page = ContactPage.objects.first()
        if contact_page:
            report.append(('ContactPage', 'hero_background_image_url', contact_page.hero_background_image_url, bool(contact_page.hero_background_image_url)))
        
        # Display report
        filled = sum(1 for _, _, _, has_url in report if has_url)
        empty = len(report) - filled
        
        self.stdout.write(f'Total image fields: {len(report)}')
        self.stdout.write(self.style.SUCCESS(f'Filled: {filled}'))
        self.stdout.write(self.style.WARNING(f'Empty: {empty}'))
        self.stdout.write(f'\nAvailable MediaAsset URLs: {len(asset_urls)}\n')
        
        self.stdout.write('\n=== Detailed Report ===\n')
        for model_name, field_name, url, has_url in report:
            status = self.style.SUCCESS('✓') if has_url else self.style.ERROR('✗')
            url_display = url[:60] + '...' if url and len(url) > 60 else (url or 'EMPTY')
            self.stdout.write(f'{status} {model_name}.{field_name}: {url_display}')

