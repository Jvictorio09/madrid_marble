from django.shortcuts import render
import json

from .content.homepage import get_homepage_content
from .content_helpers import get_homepage_content_from_db


def home(request):
    """Homepage view - uses database if available, falls back to JSON"""
    try:
        # Try to get content from database
        content = get_homepage_content_from_db()
    except:
        # Fall back to JSON file if database is not set up
        content = get_homepage_content()
    
    context = {
        "content": content
    }
    return render(request, "home.html", context)
