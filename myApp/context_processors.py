"""
Context processors to make image URLs available in all templates
"""

from myApp.models import MediaAsset


def image_urls(request):
    """
    Makes all MediaAsset URLs available in templates as 'image_urls'
    Usage in templates: {{ image_urls.0 }}, {{ image_urls.1 }}, etc.
    """
    assets = MediaAsset.objects.filter(is_active=True).order_by('-created_at')
    urls = list(assets.values_list('web_url', flat=True))
    
    return {
        'image_urls': urls,
        'image_urls_count': len(urls),
        # Also provide first few as named variables for convenience
        'image_url_1': urls[0] if len(urls) > 0 else None,
        'image_url_2': urls[1] if len(urls) > 1 else None,
        'image_url_3': urls[2] if len(urls) > 2 else None,
        'image_url_4': urls[3] if len(urls) > 3 else None,
        'image_url_5': urls[4] if len(urls) > 4 else None,
        'image_url_6': urls[5] if len(urls) > 5 else None,
        'image_url_7': urls[6] if len(urls) > 6 else None,
        'image_url_8': urls[7] if len(urls) > 7 else None,
        'image_url_9': urls[8] if len(urls) > 8 else None,
        'image_url_10': urls[9] if len(urls) > 9 else None,
    }

