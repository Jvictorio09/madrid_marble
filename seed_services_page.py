#!/usr/bin/env python
"""
Standalone script to seed Services Page data.
Run with: python seed_services_page.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

from myApp.models import ServicesPage, ServicesPageService, ServicesPageProcessStep


def seed_services_page():
    """Seed Services Page with default data"""
    print("🌱 Seeding Services Page...")
    
    # Get or create ServicesPage main object
    page, created = ServicesPage.objects.get_or_create(pk=1, defaults={
        'badge': 'Our Services',
        'title': 'Full Marble Solutions for Modern Spaces.',
        'description': 'From a single kitchen to full villa interiors and commercial fit-outs, Madrid Marble handles stone selection, technical planning, fabrication, installation, and after-care — all under one specialist team.',
        'hero_image_1_url': 'https://images.unsplash.com/photo-1600585154340-0ef3c08c0632?w=1200&auto=format&fit=crop',
        'hero_image_1_alt': 'Marble kitchen island and dining space',
        'hero_image_2_url': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=900&auto=format&fit=crop',
        'hero_image_2_alt': 'Marble bathroom vanity',
        'hero_image_3_url': 'https://images.unsplash.com/photo-1600607687920-4e2a534abf1c?w=900&auto=format&fit=crop',
        'hero_image_3_alt': 'Marble staircase and flooring',
        'hero_label': 'Kitchens • Bathrooms • Flooring • Custom Pieces',
        'solutions_title': 'Full Marble Solutions',
        'solutions_description': "Whether you're designing a new villa, upgrading a kitchen, or fitting out a commercial property, Madrid Marble provides an end-to-end solution: stone selection, technical guidance, fabrication, installation, and after-care recommendations — all managed by one specialist team.",
        'process_title': 'How We Work',
        'process_description': 'A clear, structured process from first conversation to final polish.',
    })
    
    if not created:
        # Update existing page
        page.badge = 'Our Services'
        page.title = 'Full Marble Solutions for Modern Spaces.'
        page.description = 'From a single kitchen to full villa interiors and commercial fit-outs, Madrid Marble handles stone selection, technical planning, fabrication, installation, and after-care — all under one specialist team.'
        page.hero_image_1_url = 'https://images.unsplash.com/photo-1600585154340-0ef3c08c0632?w=1200&auto=format&fit=crop'
        page.hero_image_1_alt = 'Marble kitchen island and dining space'
        page.hero_image_2_url = 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=900&auto=format&fit=crop'
        page.hero_image_2_alt = 'Marble bathroom vanity'
        page.hero_image_3_url = 'https://images.unsplash.com/photo-1600607687920-4e2a534abf1c?w=900&auto=format&fit=crop'
        page.hero_image_3_alt = 'Marble staircase and flooring'
        page.hero_label = 'Kitchens • Bathrooms • Flooring • Custom Pieces'
        page.solutions_title = 'Full Marble Solutions'
        page.solutions_description = "Whether you're designing a new villa, upgrading a kitchen, or fitting out a commercial property, Madrid Marble provides an end-to-end solution: stone selection, technical guidance, fabrication, installation, and after-care recommendations — all managed by one specialist team."
        page.process_title = 'How We Work'
        page.process_description = 'A clear, structured process from first conversation to final polish.'
        page.save()
        print("  ✓ Services Page updated")
    else:
        print("  ✓ Services Page created")
    
    # Clear existing services and create new ones
    ServicesPageService.objects.filter(services_page=page).delete()
    
    services_data = [
        {
            'service_id': 'kitchen-marble-work',
            'title': 'Kitchen Marble Work',
            'description': 'We design kitchen surfaces that feel luxurious yet practical — with careful planning for seams, sink cutouts, and appliances so you enjoy a clean, seamless look every day.',
            'icon': 'fa-solid fa-utensils',
            'image_url': 'https://images.unsplash.com/photo-1600585154340-0ef3c08c0632?w=1400&auto=format&fit=crop',
            'image_alt': 'Modern kitchen with marble island and backsplash',
            'features_json': ['Countertops', 'Islands', 'Backsplashes', 'Custom cuts & edge profiles'],
            'additional_text': '',
            'image_position': 'right',
            'sort_order': 0
        },
        {
            'service_id': 'bathroom-vanity',
            'title': 'Bathroom & Vanity Works',
            'description': 'From vanity tops and integrated basins to shower walls and floors, we create bathrooms that feel like a private spa. Our team advises on finishes, slip-resistance, and maintenance so your bathroom stays beautiful and functional over time.',
            'icon': 'fa-solid fa-bath',
            'image_url': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=1400&auto=format&fit=crop',
            'image_alt': 'Marble bathroom and vanity',
            'features_json': [],
            'additional_text': 'We pay attention to junctions, slopes, and detailing — the parts that protect against water ingress while still looking clean and minimal.',
            'image_position': 'left',
            'sort_order': 1
        },
        {
            'service_id': 'flooring-staircase',
            'title': 'Flooring & Staircase',
            'description': 'We install large-format marble flooring, wall cladding, and sculptural staircases that unify your space. Careful planning of joints, borders, and transitions ensures the final result looks intentional — not just installed.',
            'icon': 'fa-solid fa-layer-group',
            'image_url': 'https://images.unsplash.com/photo-1600607687920-4e2a534abf1c?w=1400&auto=format&fit=crop',
            'image_alt': 'Marble staircase and flooring detail',
            'features_json': [],
            'additional_text': 'Our team considers circulation routes, natural light, and how the stone will read from different angles before the first cut is made.',
            'image_position': 'right',
            'sort_order': 2
        },
        {
            'service_id': 'custom-fabrication',
            'title': 'Custom Fabrication',
            'description': 'Have a unique design in mind? We handle custom profiles, feature walls, reception counters, tabletops, and one-off statement pieces. Share your drawings or concept, and our team will help translate it into a buildable, durable marble solution.',
            'icon': 'fa-solid fa-magic',
            'image_url': '',
            'image_alt': '',
            'features_json': [],
            'additional_text': 'We support both fully detailed drawings and early-stage concepts — advising on thickness, support, fixing details, and finishes so your idea works in real life.',
            'image_position': 'right',
            'sort_order': 3
        },
    ]
    
    for service_data in services_data:
        service = ServicesPageService.objects.create(services_page=page, **service_data)
        print(f"  ✓ Created service: {service.title}")
    
    # Clear existing process steps and create new ones
    ServicesPageProcessStep.objects.filter(services_page=page).delete()
    
    process_steps_data = [
        {
            'number': '01',
            'title': 'Consult & Plan',
            'description': 'Drawings, measurements, and material direction.',
            'sort_order': 0
        },
        {
            'number': '02',
            'title': 'Select & Confirm',
            'description': 'Slab selection, finishes, and final scope.',
            'sort_order': 1
        },
        {
            'number': '03',
            'title': 'Fabricate',
            'description': 'Cut-to-size, profiling, and pre-installation checks.',
            'sort_order': 2
        },
        {
            'number': '04',
            'title': 'Install & Hand Over',
            'description': 'On-site fitting, finishing, and after-care guidance.',
            'sort_order': 3
        },
    ]
    
    for step_data in process_steps_data:
        step = ServicesPageProcessStep.objects.create(services_page=page, **step_data)
        print(f"  ✓ Created process step: {step.number} - {step.title}")
    
    print("\n✅ Services Page seeded successfully!")
    print("\n📝 You can now edit these in the dashboard:")
    print("   - Go to: Dashboard → Individual Pages → Services Page")
    print("   - Or visit: /dashboard/pages/services/")
    print("   - Service Sections: /dashboard/pages/services/sections/")
    print("   - Process Steps: /dashboard/pages/services/process/")


if __name__ == '__main__':
    seed_services_page()

