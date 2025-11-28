from django.shortcuts import render
import json

from .content.homepage import get_homepage_content
from .content_helpers import get_homepage_content_from_db


def get_content():
    """Helper function to get content from database or JSON fallback"""
    try:
        # Try to get content from database
        return get_homepage_content_from_db()
    except:
        # Fall back to JSON file if database is not set up
        return get_homepage_content()


def home(request):
    """Homepage view - uses database if available, falls back to JSON"""
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "home.html", context)


def about(request):
    """About page view"""
    from .models import AboutPage
    
    content = get_content()
    about_page = AboutPage.objects.first()
    
    context = {
        "content": content,
        "about_page": about_page
    }
    return render(request, "about.html", context)


def services(request):
    """Services page view"""
    from .models import ServicesPage
    
    content = get_content()
    services_page = ServicesPage.objects.first()
    
    context = {
        "content": content,
        "services_page": services_page
    }
    return render(request, "services.html", context)


def portfolio(request):
    """Portfolio page view"""
    from .models import PortfolioPage
    
    content = get_content()
    portfolio_page = PortfolioPage.objects.first()
    
    context = {
        "content": content,
        "portfolio_page": portfolio_page
    }
    return render(request, "portfolio.html", context)


def faq(request):
    """FAQ page view"""
    from .models import FAQPage
    
    content = get_content()
    faq_page = FAQPage.objects.first()
    
    context = {
        "content": content,
        "faq_page": faq_page
    }
    return render(request, "faq.html", context)


def contact(request):
    """Contact page view"""
    from .models import ContactPage
    
    content = get_content()
    contact_page = ContactPage.objects.first()
    
    context = {
        "content": content,
        "contact_page": contact_page
    }
    return render(request, "contact.html", context)
