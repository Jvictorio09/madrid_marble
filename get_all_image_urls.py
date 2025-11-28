"""
Utility script to extract all image URLs from the database.
Run this from the project root: python get_all_image_urls.py

This will:
1. List all image URLs from MediaAsset
2. List all image URLs currently used in the database
3. Show which fields are empty and could be populated
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

from myApp.models import (
    MediaAsset, Navigation, Hero, About, Services, Portfolio, PortfolioProject,
    AboutPage, ServicesPage, ServicesPageService, PortfolioPage, FAQPage, ContactPage
)


def get_all_image_urls():
    """Extract all image URLs from the database"""
    
    print("=" * 80)
    print("IMAGE URL EXTRACTION REPORT")
    print("=" * 80)
    
    # Get all MediaAsset URLs (these are available to use)
    media_assets = MediaAsset.objects.filter(is_active=True).order_by('-created_at')
    asset_urls = list(media_assets.values_list('web_url', flat=True))
    
    print(f"\n📦 MEDIA ASSET URLS (Available to use): {len(asset_urls)}")
    print("-" * 80)
    for i, url in enumerate(asset_urls, 1):
        print(f"{i:3d}. {url}")
    
    # Collect all URLs currently in use
    all_urls = []
    
    print(f"\n\n📋 CURRENTLY USED IMAGE URLS")
    print("-" * 80)
    
    # Navigation
    nav = Navigation.objects.first()
    if nav and nav.logo_image_url:
        all_urls.append(('Navigation.logo_image_url', nav.logo_image_url))
        print(f"✓ Navigation.logo_image_url: {nav.logo_image_url}")
    
    # Hero
    hero = Hero.objects.first()
    if hero and hero.image_url:
        all_urls.append(('Hero.image_url', hero.image_url))
        print(f"✓ Hero.image_url: {hero.image_url}")
    
    # Services
    services = Services.objects.first()
    if services and services.image_url:
        all_urls.append(('Services.image_url', services.image_url))
        print(f"✓ Services.image_url: {services.image_url}")
    
    # Portfolio
    portfolio = Portfolio.objects.first()
    if portfolio and portfolio.feature_image_url:
        all_urls.append(('Portfolio.feature_image_url', portfolio.feature_image_url))
        print(f"✓ Portfolio.feature_image_url: {portfolio.feature_image_url}")
    
    # Portfolio Projects
    projects = PortfolioProject.objects.filter(is_active=True)
    for project in projects:
        if project.image_url:
            all_urls.append((f'PortfolioProject#{project.id}.image_url', project.image_url))
            print(f"✓ PortfolioProject#{project.id}.image_url: {project.image_url}")
    
    # About Page
    about_page = AboutPage.objects.first()
    if about_page:
        if about_page.hero_image_url:
            all_urls.append(('AboutPage.hero_image_url', about_page.hero_image_url))
            print(f"✓ AboutPage.hero_image_url: {about_page.hero_image_url}")
        if about_page.workshop_image_url:
            all_urls.append(('AboutPage.workshop_image_url', about_page.workshop_image_url))
            print(f"✓ AboutPage.workshop_image_url: {about_page.workshop_image_url}")
    
    # Services Page
    services_page = ServicesPage.objects.first()
    if services_page:
        if services_page.hero_image_1_url:
            all_urls.append(('ServicesPage.hero_image_1_url', services_page.hero_image_1_url))
            print(f"✓ ServicesPage.hero_image_1_url: {services_page.hero_image_1_url}")
        if services_page.hero_image_2_url:
            all_urls.append(('ServicesPage.hero_image_2_url', services_page.hero_image_2_url))
            print(f"✓ ServicesPage.hero_image_2_url: {services_page.hero_image_2_url}")
        if services_page.hero_image_3_url:
            all_urls.append(('ServicesPage.hero_image_3_url', services_page.hero_image_3_url))
            print(f"✓ ServicesPage.hero_image_3_url: {services_page.hero_image_3_url}")
        
        # Services Page Services
        for service in services_page.services.all():
            if service.image_url:
                all_urls.append((f'ServicesPageService#{service.id}.image_url', service.image_url))
                print(f"✓ ServicesPageService#{service.id}.image_url: {service.image_url}")
    
    # Portfolio Page
    portfolio_page = PortfolioPage.objects.first()
    if portfolio_page:
        if portfolio_page.hero_image_1_url:
            all_urls.append(('PortfolioPage.hero_image_1_url', portfolio_page.hero_image_1_url))
            print(f"✓ PortfolioPage.hero_image_1_url: {portfolio_page.hero_image_1_url}")
        if portfolio_page.hero_image_2_url:
            all_urls.append(('PortfolioPage.hero_image_2_url', portfolio_page.hero_image_2_url))
            print(f"✓ PortfolioPage.hero_image_2_url: {portfolio_page.hero_image_2_url}")
        if portfolio_page.hero_image_3_url:
            all_urls.append(('PortfolioPage.hero_image_3_url', portfolio_page.hero_image_3_url))
            print(f"✓ PortfolioPage.hero_image_3_url: {portfolio_page.hero_image_3_url}")
        if portfolio_page.residential_featured_image_url:
            all_urls.append(('PortfolioPage.residential_featured_image_url', portfolio_page.residential_featured_image_url))
            print(f"✓ PortfolioPage.residential_featured_image_url: {portfolio_page.residential_featured_image_url}")
        if portfolio_page.commercial_featured_image_url:
            all_urls.append(('PortfolioPage.commercial_featured_image_url', portfolio_page.commercial_featured_image_url))
            print(f"✓ PortfolioPage.commercial_featured_image_url: {portfolio_page.commercial_featured_image_url}")
    
    # FAQ Page
    faq_page = FAQPage.objects.first()
    if faq_page and faq_page.hero_image_url:
        all_urls.append(('FAQPage.hero_image_url', faq_page.hero_image_url))
        print(f"✓ FAQPage.hero_image_url: {faq_page.hero_image_url}")
    
    # Contact Page
    contact_page = ContactPage.objects.first()
    if contact_page and contact_page.hero_background_image_url:
        all_urls.append(('ContactPage.hero_background_image_url', contact_page.hero_background_image_url))
        print(f"✓ ContactPage.hero_background_image_url: {contact_page.hero_background_image_url}")
    
    # Summary
    print(f"\n\n📊 SUMMARY")
    print("-" * 80)
    print(f"Available MediaAsset URLs: {len(asset_urls)}")
    print(f"Currently used URLs: {len(all_urls)}")
    
    # Show empty fields that could be populated
    print(f"\n\n⚠️  EMPTY FIELDS (Could be populated)")
    print("-" * 80)
    empty_fields = []
    
    nav = Navigation.objects.first()
    if nav and not nav.logo_image_url:
        empty_fields.append('Navigation.logo_image_url')
        print("✗ Navigation.logo_image_url: EMPTY")
    
    hero = Hero.objects.first()
    if hero and not hero.image_url:
        empty_fields.append('Hero.image_url')
        print("✗ Hero.image_url: EMPTY")
    
    services = Services.objects.first()
    if services and not services.image_url:
        empty_fields.append('Services.image_url')
        print("✗ Services.image_url: EMPTY")
    
    portfolio = Portfolio.objects.first()
    if portfolio and not portfolio.feature_image_url:
        empty_fields.append('Portfolio.feature_image_url')
        print("✗ Portfolio.feature_image_url: EMPTY")
    
    projects = PortfolioProject.objects.filter(image_url__isnull=True) | PortfolioProject.objects.filter(image_url='')
    for project in projects[:5]:
        empty_fields.append(f'PortfolioProject#{project.id}.image_url')
        print(f"✗ PortfolioProject#{project.id}.image_url: EMPTY")
    
    about_page = AboutPage.objects.first()
    if about_page:
        if not about_page.hero_image_url:
            empty_fields.append('AboutPage.hero_image_url')
            print("✗ AboutPage.hero_image_url: EMPTY")
        if not about_page.workshop_image_url:
            empty_fields.append('AboutPage.workshop_image_url')
            print("✗ AboutPage.workshop_image_url: EMPTY")
    
    services_page = ServicesPage.objects.first()
    if services_page:
        if not services_page.hero_image_1_url:
            empty_fields.append('ServicesPage.hero_image_1_url')
            print("✗ ServicesPage.hero_image_1_url: EMPTY")
        if not services_page.hero_image_2_url:
            empty_fields.append('ServicesPage.hero_image_2_url')
            print("✗ ServicesPage.hero_image_2_url: EMPTY")
        if not services_page.hero_image_3_url:
            empty_fields.append('ServicesPage.hero_image_3_url')
            print("✗ ServicesPage.hero_image_3_url: EMPTY")
    
    portfolio_page = PortfolioPage.objects.first()
    if portfolio_page:
        if not portfolio_page.hero_image_1_url:
            empty_fields.append('PortfolioPage.hero_image_1_url')
            print("✗ PortfolioPage.hero_image_1_url: EMPTY")
        if not portfolio_page.hero_image_2_url:
            empty_fields.append('PortfolioPage.hero_image_2_url')
            print("✗ PortfolioPage.hero_image_2_url: EMPTY")
        if not portfolio_page.hero_image_3_url:
            empty_fields.append('PortfolioPage.hero_image_3_url')
            print("✗ PortfolioPage.hero_image_3_url: EMPTY")
        if not portfolio_page.residential_featured_image_url:
            empty_fields.append('PortfolioPage.residential_featured_image_url')
            print("✗ PortfolioPage.residential_featured_image_url: EMPTY")
        if not portfolio_page.commercial_featured_image_url:
            empty_fields.append('PortfolioPage.commercial_featured_image_url')
            print("✗ PortfolioPage.commercial_featured_image_url: EMPTY")
    
    faq_page = FAQPage.objects.first()
    if faq_page and not faq_page.hero_image_url:
        empty_fields.append('FAQPage.hero_image_url')
        print("✗ FAQPage.hero_image_url: EMPTY")
    
    contact_page = ContactPage.objects.first()
    if contact_page and not contact_page.hero_background_image_url:
        empty_fields.append('ContactPage.hero_background_image_url')
        print("✗ ContactPage.hero_background_image_url: EMPTY")
    
    print(f"\n\n💡 QUICK COPY - All Available URLs (for templates)")
    print("-" * 80)
    print("Copy these URLs to use in your templates:")
    for i, url in enumerate(asset_urls, 1):
        print(f'url_{i} = "{url}"')
    
    print(f"\n\n✅ Done! Found {len(asset_urls)} available URLs and {len(empty_fields)} empty fields.")
    print(f"\nTo auto-populate empty fields, run: python manage.py populate_image_urls --populate")


if __name__ == '__main__':
    get_all_image_urls()

