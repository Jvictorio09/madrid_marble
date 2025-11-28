"""
Simple script to get all image URLs from database as a Python dictionary.
Run: python get_image_urls_dict.py

This outputs a dictionary you can copy-paste and use anywhere.
"""

import os
import sys
import django
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

from myApp.models import MediaAsset


def get_urls_dict():
    """Get all image URLs as a simple dictionary"""
    
    # Get all active MediaAsset URLs
    assets = MediaAsset.objects.filter(is_active=True).order_by('-created_at')
    
    urls = {
        'all_urls': list(assets.values_list('web_url', flat=True)),
        'urls_by_index': {}
    }
    
    # Create indexed access
    for i, asset in enumerate(assets, 1):
        urls['urls_by_index'][f'url_{i}'] = asset.web_url
        urls['urls_by_index'][f'url_{i}_thumb'] = asset.thumb_url
    
    # Also create a simple list for easy access
    urls['url_list'] = list(assets.values_list('web_url', flat=True))
    
    print("=" * 80)
    print("IMAGE URLS DICTIONARY")
    print("=" * 80)
    print(f"\nFound {len(urls['all_urls'])} active image URLs\n")
    
    print("=" * 80)
    print("PYTHON DICTIONARY (Copy this):")
    print("=" * 80)
    print(json.dumps(urls, indent=2))
    
    print("\n" + "=" * 80)
    print("SIMPLE LIST (Copy this):")
    print("=" * 80)
    print("IMAGE_URLS = [")
    for url in urls['all_urls']:
        print(f'    "{url}",')
    print("]")
    
    print("\n" + "=" * 80)
    print("USAGE EXAMPLES:")
    print("=" * 80)
    print("# In templates, you can use:")
    print("# {{ IMAGE_URLS.0 }} for first URL")
    print("# {{ IMAGE_URLS.1 }} for second URL")
    print("# etc.")
    
    print(f"\n✅ Total URLs available: {len(urls['all_urls'])}")
    
    return urls


if __name__ == '__main__':
    get_urls_dict()

