#!/usr/bin/env python
"""
Standalone script to seed contact info data.
Run with: python seed_contact_info.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

from myApp.models import Contact, ContactInfo, ContactFormField, SocialLink

def seed_contact_info():
    """Seed contact information with default data"""
    print("🌱 Seeding Contact Information...")
    
    # Get or create Contact main object
    contact, created = Contact.objects.get_or_create(pk=1, defaults={
        'badge': 'CONTACT',
        'heading': "Let's turn your ideas into solid marble reality.",
        'description': 'Share your drawings, inspiration photos, or even a rough concept — our team will help you refine it into a buildable plan with the right stone, finish, and budget.',
        'intro_text': 'For project inquiries and showroom appointments, share your details below. We\'ll review your scope and respond within 24 hours with tailored stone recommendations, next steps, and available visit slots.',
        'background_image': 'https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=1400&q=70',
        'socials_label': 'FOLLOW MADRID MARBLE',
        'form_submit_label': 'Submit inquiry',
        'form_disclaimer': 'By submitting this form, you agree to be contacted by the Madrid Marble team regarding your project.',
    })
    
    if not created:
        contact.badge = 'CONTACT'
        contact.heading = "Let's turn your ideas into solid marble reality."
        contact.description = 'Share your drawings, inspiration photos, or even a rough concept — our team will help you refine it into a buildable plan with the right stone, finish, and budget.'
        contact.intro_text = 'For project inquiries and showroom appointments, share your details below. We\'ll review your scope and respond within 24 hours with tailored stone recommendations, next steps, and available visit slots.'
        contact.background_image = 'https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=1400&q=70'
        contact.socials_label = 'FOLLOW MADRID MARBLE'
        contact.form_submit_label = 'Submit inquiry'
        contact.form_disclaimer = 'By submitting this form, you agree to be contacted by the Madrid Marble team regarding your project.'
        contact.save()
        print("  ✓ Contact section updated")
    else:
        print("  ✓ Contact section created")
    
    # Clear existing contact info and create new ones
    ContactInfo.objects.all().delete()
    
    contact_info_items = [
        {
            'label': 'PHONE',
            'text': '+971 55 221 8761',
            'href': 'tel:+971552218761',
            'info_type': 'phone',
            'sort_order': 0
        },
        {
            'label': 'WHATSAPP',
            'text': '+971 55 221 8761',
            'href': 'https://wa.me/971552218761',
            'info_type': 'whatsapp',
            'sort_order': 1
        },
        {
            'label': 'EMAIL',
            'text': 'hello@madridmarble.ae',
            'href': 'mailto:hello@madridmarble.ae',
            'info_type': 'email',
            'sort_order': 2
        },
        {
            'label': 'SHOWROOM & WAREHOUSE',
            'text': 'Sharjah',
            'href': '',
            'info_type': 'address',
            'sort_order': 3
        },
    ]
    
    for info_data in contact_info_items:
        ContactInfo.objects.create(**info_data)
        print(f"  ✓ Created {info_data['info_type'].upper()}: {info_data['text']}")
    
    # Seed contact form fields if they don't exist
    if not ContactFormField.objects.exists():
        form_fields = [
            {
                'name': 'name',
                'label': 'Name',
                'field_type': 'text',
                'placeholder': 'Your full name',
                'span': 1,
                'required': True,
                'sort_order': 0
            },
            {
                'name': 'email',
                'label': 'Email',
                'field_type': 'email',
                'placeholder': 'name@company.com',
                'span': 1,
                'required': True,
                'sort_order': 1
            },
            {
                'name': 'phone',
                'label': 'Phone',
                'field_type': 'tel',
                'placeholder': '+971 50 000 0000',
                'span': 2,
                'required': True,
                'sort_order': 2
            },
            {
                'name': 'project_type',
                'label': 'Project type',
                'field_type': 'text',
                'placeholder': 'Villa, apartment, hotel, commercial…',
                'span': 1,
                'required': True,
                'sort_order': 3
            },
            {
                'name': 'project_location',
                'label': 'Project location',
                'field_type': 'text',
                'placeholder': 'Dubai Hills, Palm Jumeirah, JVC…',
                'span': 1,
                'required': True,
                'sort_order': 4
            },
            {
                'name': 'project_details',
                'label': 'Project details',
                'field_type': 'textarea',
                'placeholder': 'Share your drawings, scope, timelines, and preferred marble finishes.',
                'rows': 5,
                'span': 2,
                'required': True,
                'sort_order': 5
            },
        ]
        
        for field_data in form_fields:
            ContactFormField.objects.create(contact=contact, **field_data)
        print(f"  ✓ Created {len(form_fields)} form fields")
    
    # Seed social links if they don't exist
    if not SocialLink.objects.exists():
        social_links = [
            {
                'icon': 'fa-brands fa-instagram',
                'href': '#',
                'sort_order': 0
            },
            {
                'icon': 'fa-brands fa-tiktok',
                'href': '#',
                'sort_order': 1
            },
            {
                'icon': 'fa-brands fa-linkedin-in',
                'href': '#',
                'sort_order': 2
            },
        ]
        
        for link_data in social_links:
            SocialLink.objects.create(**link_data)
        print(f"  ✓ Created {len(social_links)} social links")
    
    print("\n✅ Contact information seeded successfully!")
    print("\n📝 You can now edit these in the dashboard:")
    print("   - Go to: Dashboard → Landing Page → Contact Section → Contact Info")
    print("   - Or visit: /dashboard/contact/info/")


if __name__ == '__main__':
    seed_contact_info()





