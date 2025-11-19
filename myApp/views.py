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
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "about.html", context)


def services(request):
    """Services page view"""
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "services.html", context)


def portfolio(request):
    """Portfolio page view"""
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "portfolio.html", context)


def faq(request):
    """FAQ page view"""
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "faq.html", context)


def contact(request):
    """Contact page view"""
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "contact.html", context)
