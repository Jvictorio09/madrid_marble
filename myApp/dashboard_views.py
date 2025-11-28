from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from .models import (
    SEO, Navigation, Hero, About, Stat, Service, Services, 
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer, MediaAsset,
    Promise, PromiseCard, FeaturedServices, FeaturedService, WhyTrust, WhyTrustFactor,
    AboutPage, AboutTimelineItem, AboutMissionCard, AboutFeatureCard, AboutValue, AboutTeamMember,
    ServicesPage, ServicesPageService, ServicesPageProcessStep,
    PortfolioPage, PortfolioPageCategory,
    FAQPage, FAQPageSection, FAQPageQuestion, FAQPageTip,
    ContactPage
)
from .utils.cloudinary_utils import smart_compress_to_bytes, upload_to_cloudinary, TARGET_BYTES
import json


@login_required
def dashboard_home(request):
    """Main dashboard page"""
    context = {
        'seo': SEO.objects.first(),
        'navigation': Navigation.objects.first(),
        'hero': Hero.objects.first(),
        'about': About.objects.first(),
        'stats': Stat.objects.all(),
        'services_section': Services.objects.first(),
        'services': Service.objects.all(),
        'portfolio': Portfolio.objects.first(),
        'portfolio_projects': PortfolioProject.objects.all(),
        'testimonials': Testimonial.objects.all(),
        'faq_section': FAQSection.objects.first(),
        'faqs': FAQ.objects.all(),
        'contact': Contact.objects.first(),
        'contact_info': ContactInfo.objects.all(),
        'social_links': SocialLink.objects.all(),
        'footer': Footer.objects.first(),
    }
    return render(request, 'dashboard/index.html', context)


# Image Upload Views
@login_required
@require_POST
@csrf_exempt
def upload_image(request):
    """Handle image upload with automatic compression and Cloudinary upload."""
    if 'file' not in request.FILES:
        return JsonResponse({"success": False, "error": "No file provided"})
    
    file = request.FILES['file']
    folder = request.POST.get('folder', 'madrid_marble/uploads')
    tags = request.POST.get('tags', '').split(',') if request.POST.get('tags') else []
    
    try:
        # Compress if needed
        if file.size > TARGET_BYTES:
            file_bytes = smart_compress_to_bytes(file)
        else:
            file_bytes = file.read()
        
        # Generate public_id from filename
        public_id = slugify(file.name.rsplit('.', 1)[0])
        
        # Upload to Cloudinary
        result, web_url, thumb_url = upload_to_cloudinary(
            file_bytes=file_bytes,
            folder=folder,
            public_id=public_id,
            tags=tags
        )
        
        # Store in database
        asset = MediaAsset.objects.create(
            title=file.name,
            public_id=result.get("public_id"),
            secure_url=result.get("secure_url"),
            web_url=web_url,
            thumb_url=thumb_url,
            bytes_size=result.get("bytes", 0),
            width=result.get("width", 0),
            height=result.get("height", 0),
            format=result.get("format", ""),
            tags_csv=",".join(tags) if tags else "",
        )
        
        return JsonResponse({
            "success": True,
            "id": asset.id,
            "title": asset.title,
            "secure_url": asset.secure_url,
            "web_url": asset.web_url,
            "thumb_url": asset.thumb_url,
            "public_id": asset.public_id,
            "width": asset.width,
            "height": asset.height,
            "format": asset.format,
            "bytes": asset.bytes_size
        })
    
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def gallery(request):
    """Image gallery view"""
    assets = MediaAsset.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'dashboard/gallery.html', {'assets': assets})


# SEO Management
@login_required
def seo_edit(request):
    """Edit SEO settings"""
    seo = SEO.objects.first()
    if not seo:
        seo = SEO.objects.create(
            title="Premium Marble Supplier in UAE | Slabs, Cut-to-Size & Installation",
            description="Madrid Marble supplies premium slabs and tiles in the UAE.",
            canonical="https://madridmarble-production.up.railway.app/",
        )
    
    if request.method == 'POST':
        seo.title = request.POST.get('title', '')
        seo.description = request.POST.get('description', '')
        seo.canonical = request.POST.get('canonical', '')
        seo.og_title = request.POST.get('og_title', '')
        seo.og_description = request.POST.get('og_description', '')
        seo.og_image = request.POST.get('og_image', '')
        seo.favicon = request.POST.get('favicon', '')
        seo.preload_hero = request.POST.get('preload_hero', '')
        seo.save()
        messages.success(request, 'SEO settings updated successfully!')
        return redirect('dashboard:seo_edit')
    
    return render(request, 'dashboard/seo_edit.html', {'seo': seo})


# Navigation Management
@login_required
def navigation_edit(request):
    """Edit navigation settings"""
    nav = Navigation.objects.first()
    if not nav:
        nav = Navigation.objects.create(
            logo_text="MM",
            logo_image_url="",
            brand="Madrid Marble",
            links_json=[],
            cta_label="Start a project",
            cta_href="#contact"
        )
    
    if request.method == 'POST':
        nav.logo_text = request.POST.get('logo_text', '')
        nav.logo_image_url = request.POST.get('logo_image_url', '')
        nav.brand = request.POST.get('brand', '')
        nav.cta_label = request.POST.get('cta_label', '')
        nav.cta_href = request.POST.get('cta_href', '')
        
        # Parse links JSON
        links_json_str = request.POST.get('links_json', '[]')
        try:
            nav.links_json = json.loads(links_json_str)
        except:
            nav.links_json = []
        
        nav.save()
        messages.success(request, 'Navigation settings updated successfully!')
        return redirect('dashboard:navigation_edit')
    
    return render(request, 'dashboard/navigation_edit.html', {'nav': nav})


# Hero Management
@login_required
def hero_edit(request):
    """Edit hero section"""
    hero = Hero.objects.first()
    if not hero:
        hero = Hero.objects.create(
            headline="Your trusted partner for quality marble works in the UAE",
            description="Madrid Marble delivers luxury marble installation...",
        )
    
    if request.method == 'POST':
        hero.badge = request.POST.get('badge', '')
        hero.eyebrow = request.POST.get('eyebrow', '')
        hero.headline = request.POST.get('headline', '')
        hero.description = request.POST.get('description', '')
        hero.image_url = request.POST.get('image_url', '')
        hero.image_alt = request.POST.get('image_alt', '')
        hero.primary_cta_label = request.POST.get('primary_cta_label', '')
        hero.primary_cta_href = request.POST.get('primary_cta_href', '')
        hero.primary_cta_icon = request.POST.get('primary_cta_icon', '')
        hero.secondary_cta_label = request.POST.get('secondary_cta_label', '')
        hero.secondary_cta_href = request.POST.get('secondary_cta_href', '')
        hero.testimonial_quote = request.POST.get('testimonial_quote', '')
        hero.testimonial_name = request.POST.get('testimonial_name', '')
        hero.testimonial_meta = request.POST.get('testimonial_meta', '')
        hero.testimonial_stars = int(request.POST.get('testimonial_stars', 5))
        
        # Parse stats JSON
        stats_json_str = request.POST.get('stats_json', '[]')
        try:
            hero.stats_json = json.loads(stats_json_str)
        except:
            hero.stats_json = []
        
        hero.save()
        messages.success(request, 'Hero section updated successfully!')
        return redirect('dashboard:hero_edit')
    
    # Format stats_json for display
    import json as json_lib
    stats_json_str = json_lib.dumps(hero.stats_json, indent=2) if hero.stats_json else '[]'
    
    return render(request, 'dashboard/hero_edit.html', {
        'hero': hero,
        'stats_json_str': stats_json_str
    })


# About Management
@login_required
def about_edit(request):
    """Edit about section"""
    about = About.objects.first()
    if not about:
        about = About.objects.create(
            title="Marble & Stone Specialists",
            copy_json=[],
            gallery_json=[]
        )
    
    if request.method == 'POST':
        about.badge = request.POST.get('badge', '')
        about.title = request.POST.get('title', '')
        
        # Parse copy JSON
        copy_json_str = request.POST.get('copy_json', '[]').strip()
        if not copy_json_str:
            copy_json_str = '[]'
        try:
            parsed_copy = json.loads(copy_json_str)
            # Ensure it's a list
            if not isinstance(parsed_copy, list):
                messages.error(request, 'Copy JSON must be an array. Using empty array.')
                about.copy_json = []
            else:
                about.copy_json = parsed_copy
        except json.JSONDecodeError as e:
            messages.error(request, f'Invalid JSON in Copy field: {str(e)}. Using empty array.')
            about.copy_json = []
        except Exception as e:
            messages.error(request, f'Error parsing Copy JSON: {str(e)}. Using empty array.')
            about.copy_json = []
        
        # Parse gallery JSON
        gallery_json_str = request.POST.get('gallery_json', '[]').strip()
        if not gallery_json_str:
            gallery_json_str = '[]'
        try:
            parsed_gallery = json.loads(gallery_json_str)
            # Ensure it's a list
            if not isinstance(parsed_gallery, list):
                messages.error(request, 'Gallery JSON must be an array. Using empty array.')
                about.gallery_json = []
            else:
                about.gallery_json = parsed_gallery
        except json.JSONDecodeError as e:
            messages.error(request, f'Invalid JSON in Gallery field: {str(e)}. Using empty array.')
            about.gallery_json = []
        except Exception as e:
            messages.error(request, f'Error parsing Gallery JSON: {str(e)}. Using empty array.')
            about.gallery_json = []
        
        about.save()
        messages.success(request, 'About section updated successfully!')
        return redirect('dashboard:about_edit')
    
    # Convert gallery_json and copy_json to JSON strings for template
    import json as json_lib
    gallery_json_str = json_lib.dumps(about.gallery_json) if about.gallery_json else '[]'
    copy_json_str = json_lib.dumps(about.copy_json, indent=2) if about.copy_json else '[]'
    
    return render(request, 'dashboard/about_edit.html', {
        'about': about,
        'gallery_json_str': gallery_json_str,
        'copy_json_str': copy_json_str
    })


# Stats Management
@login_required
def stats_list(request):
    """List all stats"""
    stats = Stat.objects.all().order_by('sort_order')
    return render(request, 'dashboard/stats_list.html', {'stats': stats})


@login_required
def stat_edit(request, stat_id=None):
    """Create or edit stat"""
    if stat_id:
        stat = get_object_or_404(Stat, id=stat_id)
    else:
        stat = None
    
    if request.method == 'POST':
        if not stat:
            stat = Stat()
        stat.value = request.POST.get('value', '')
        stat.label = request.POST.get('label', '')
        stat.description = request.POST.get('description', '')
        stat.sort_order = int(request.POST.get('sort_order', 0))
        stat.save()
        messages.success(request, f'Stat {"updated" if stat_id else "created"} successfully!')
        return redirect('dashboard:stats_list')
    
    return render(request, 'dashboard/stat_edit.html', {'stat': stat})


@login_required
def stat_delete(request, stat_id):
    """Delete stat"""
    stat = get_object_or_404(Stat, id=stat_id)
    stat.delete()
    messages.success(request, 'Stat deleted successfully!')
    return redirect('dashboard:stats_list')


# Services Management
@login_required
def services_section_edit(request):
    """Edit services section configuration"""
    services_section = Services.objects.first()
    if not services_section:
        services_section = Services.objects.create(
            title="What we do",
            description="Comprehensive marble fabrication & installation...",
        )
    
    if request.method == 'POST':
        services_section.title = request.POST.get('title', '')
        services_section.description = request.POST.get('description', '')
        services_section.image_url = request.POST.get('image_url', '')
        services_section.image_alt = request.POST.get('image_alt', '')
        services_section.save()
        messages.success(request, 'Services section updated successfully!')
        return redirect('dashboard:services_section_edit')
    
    return render(request, 'dashboard/services_section_edit.html', {'services_section': services_section})


@login_required
def services_list(request):
    """List all services"""
    services = Service.objects.all().order_by('sort_order')
    return render(request, 'dashboard/services_list.html', {'services': services})


@login_required
def service_edit(request, service_id=None):
    """Create or edit service"""
    if service_id:
        service = get_object_or_404(Service, id=service_id)
    else:
        service = None
    
    if request.method == 'POST':
        if not service:
            service = Service()
        service.title = request.POST.get('title', '')
        service.description = request.POST.get('description', '')
        service.icon = request.POST.get('icon', '')
        service.is_open = request.POST.get('is_open') == 'on'
        service.sort_order = int(request.POST.get('sort_order', 0))
        service.save()
        messages.success(request, f'Service {"updated" if service_id else "created"} successfully!')
        return redirect('dashboard:services_list')
    
    return render(request, 'dashboard/service_edit.html', {'service': service})


@login_required
def service_delete(request, service_id):
    """Delete service"""
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, 'Service deleted successfully!')
    return redirect('dashboard:services_list')


# Portfolio Management
@login_required
def portfolio_edit(request):
    """Edit portfolio section"""
    portfolio = Portfolio.objects.first()
    if not portfolio:
        portfolio = Portfolio.objects.create(
            heading="Get inspired by our projects",
            description="Explore how our premium marble slabs supplier UAE team crafts enduring interiors...",
        )
    
    if request.method == 'POST':
        portfolio.heading = request.POST.get('heading', '')
        portfolio.description = request.POST.get('description', '')
        portfolio.feature_image_url = request.POST.get('feature_image_url', '')
        portfolio.feature_image_alt = request.POST.get('feature_image_alt', '')
        portfolio.feature_title = request.POST.get('feature_title', '')
        portfolio.feature_description = request.POST.get('feature_description', '')
        portfolio.feature_testimonial_quote = request.POST.get('feature_testimonial_quote', '')
        portfolio.feature_testimonial_author = request.POST.get('feature_testimonial_author', '')
        portfolio.feature_cta_label = request.POST.get('feature_cta_label', '')
        portfolio.feature_cta_href = request.POST.get('feature_cta_href', '')
        portfolio.feature_cta_icon = request.POST.get('feature_cta_icon', '')
        
        # Parse tags JSON
        tags_json_str = request.POST.get('feature_tags_json', '[]')
        try:
            portfolio.feature_tags_json = json.loads(tags_json_str)
        except:
            portfolio.feature_tags_json = []
        
        portfolio.save()
        messages.success(request, 'Portfolio section updated successfully!')
        return redirect('dashboard:portfolio_edit')
    
    return render(request, 'dashboard/portfolio_edit.html', {'portfolio': portfolio})


@login_required
def portfolio_projects_list(request):
    """List all portfolio projects"""
    # Show all projects (active and inactive) in dashboard
    projects = PortfolioProject.objects.all().order_by('sort_order')
    return render(request, 'dashboard/portfolio_projects_list.html', {'projects': projects})


@login_required
def portfolio_project_edit(request, project_id=None):
    """Create or edit portfolio project"""
    if project_id:
        project = get_object_or_404(PortfolioProject, id=project_id)
    else:
        project = None
    
    if request.method == 'POST':
        if not project:
            project = PortfolioProject()
        project.title = request.POST.get('title', '')
        project.description = request.POST.get('description', '')
        project.image_url = request.POST.get('image_url', '')
        project.image_alt = request.POST.get('image_alt', '')
        project.sort_order = int(request.POST.get('sort_order', 0))
        project.is_active = request.POST.get('is_active') == 'on'
        project.save()
        messages.success(request, f'Portfolio project {"updated" if project_id else "created"} successfully!')
        return redirect('dashboard:portfolio_projects_list')
    
    return render(request, 'dashboard/portfolio_project_edit.html', {'project': project})


@login_required
def portfolio_project_toggle_active(request, project_id):
    """Toggle project active status"""
    project = get_object_or_404(PortfolioProject, id=project_id)
    project.is_active = not project.is_active
    project.save()
    status = "activated" if project.is_active else "deactivated"
    messages.success(request, f'Portfolio project {status} successfully!')
    return redirect('dashboard:portfolio_projects_list')


@login_required
def portfolio_project_delete(request, project_id):
    """Delete portfolio project"""
    project = get_object_or_404(PortfolioProject, id=project_id)
    project.delete()
    messages.success(request, 'Portfolio project deleted successfully!')
    return redirect('dashboard:portfolio_projects_list')


# Contact Management
@login_required
def contact_edit(request):
    """Edit contact section"""
    contact = Contact.objects.first()
    if not contact:
        contact = Contact.objects.create(
            badge="CONTACT",
            heading="Speak with the Madrid Marble team",
            description="Share your drawings, timelines, and project details...",
            intro_text="For project inquiries and showroom appointments...",
            socials_label="FOLLOW MADRID MARBLE",
            form_submit_label="Submit inquiry",
            form_disclaimer="By submitting this form, you agree to be contacted by the Madrid Marble team regarding your project."
        )
    
    if request.method == 'POST':
        contact.badge = request.POST.get('badge', '')
        contact.heading = request.POST.get('heading', '')
        contact.description = request.POST.get('description', '')
        contact.intro_text = request.POST.get('intro_text', '')
        contact.background_image = request.POST.get('background_image', '')
        contact.socials_label = request.POST.get('socials_label', '')
        contact.form_submit_label = request.POST.get('form_submit_label', '')
        contact.form_disclaimer = request.POST.get('form_disclaimer', '')
        contact.save()
        messages.success(request, 'Contact section updated successfully!')
        return redirect('dashboard:contact_edit')
    
    return render(request, 'dashboard/contact_edit.html', {'contact': contact})


@login_required
def contact_info_list(request):
    """List all contact info items"""
    info_items = ContactInfo.objects.all().order_by('sort_order')
    return render(request, 'dashboard/contact_info_list.html', {'info_items': info_items})


@login_required
def contact_info_edit(request, info_id=None):
    """Create or edit contact info"""
    if info_id:
        info = get_object_or_404(ContactInfo, id=info_id)
    else:
        info = None
    
    if request.method == 'POST':
        if not info:
            info = ContactInfo()
        info.label = request.POST.get('label', '')
        info.text = request.POST.get('text', '')
        info.href = request.POST.get('href', '')
        info.info_type = request.POST.get('info_type', 'address')
        info.sort_order = int(request.POST.get('sort_order', 0))
        info.save()
        messages.success(request, f'Contact info {"updated" if info_id else "created"} successfully!')
        return redirect('dashboard:contact_info_list')
    
    return render(request, 'dashboard/contact_info_edit.html', {'info': info})


@login_required
def contact_info_delete(request, info_id):
    """Delete contact info"""
    info = get_object_or_404(ContactInfo, id=info_id)
    info.delete()
    messages.success(request, 'Contact info deleted successfully!')
    return redirect('dashboard:contact_info_list')


@login_required
def contact_form_fields_list(request):
    """List all contact form fields"""
    fields = ContactFormField.objects.all().order_by('sort_order')
    contact = Contact.objects.first()
    return render(request, 'dashboard/contact_form_fields_list.html', {'fields': fields, 'contact': contact})


@login_required
def contact_form_field_edit(request, field_id=None):
    """Create or edit contact form field"""
    contact = Contact.objects.first()
    if not contact:
        contact = Contact.objects.create(
            badge="CONTACT",
            heading="Speak with the Madrid Marble team",
            description="Share your drawings, timelines, and project details...",
        )
    
    if field_id:
        field = get_object_or_404(ContactFormField, id=field_id)
    else:
        field = None
    
    if request.method == 'POST':
        if not field:
            field = ContactFormField(contact=contact)
        field.name = request.POST.get('name', '')
        field.label = request.POST.get('label', '')
        field.field_type = request.POST.get('field_type', 'text')
        field.placeholder = request.POST.get('placeholder', '')
        field.span = int(request.POST.get('span', 1))
        field.rows = int(request.POST.get('rows', 5))
        field.required = request.POST.get('required') == 'on'
        field.sort_order = int(request.POST.get('sort_order', 0))
        field.save()
        messages.success(request, f'Form field {"updated" if field_id else "created"} successfully!')
        return redirect('dashboard:contact_form_fields_list')
    
    return render(request, 'dashboard/contact_form_field_edit.html', {'field': field, 'contact': contact})


@login_required
def contact_form_field_delete(request, field_id):
    """Delete contact form field"""
    field = get_object_or_404(ContactFormField, id=field_id)
    field.delete()
    messages.success(request, 'Form field deleted successfully!')
    return redirect('dashboard:contact_form_fields_list')


@login_required
def social_links_list(request):
    """List all social links"""
    links = SocialLink.objects.all().order_by('sort_order')
    return render(request, 'dashboard/social_links_list.html', {'links': links})


@login_required
def social_link_edit(request, link_id=None):
    """Create or edit social link"""
    if link_id:
        link = get_object_or_404(SocialLink, id=link_id)
    else:
        link = None
    
    if request.method == 'POST':
        if not link:
            link = SocialLink()
        link.icon = request.POST.get('icon', '')
        link.href = request.POST.get('href', '')
        link.sort_order = int(request.POST.get('sort_order', 0))
        link.save()
        messages.success(request, f'Social link {"updated" if link_id else "created"} successfully!')
        return redirect('dashboard:social_links_list')
    
    return render(request, 'dashboard/social_link_edit.html', {'link': link})


@login_required
def social_link_delete(request, link_id):
    """Delete social link"""
    link = get_object_or_404(SocialLink, id=link_id)
    link.delete()
    messages.success(request, 'Social link deleted successfully!')
    return redirect('dashboard:social_links_list')


# Footer Management
@login_required
def footer_edit(request):
    """Edit footer settings"""
    footer = Footer.objects.first()
    if not footer:
        footer = Footer.objects.create(
            logo_text="MM",
            note="Madrid Marble. All rights reserved.",
            links_json=[]
        )
    
    if request.method == 'POST':
        footer.logo_text = request.POST.get('logo_text', '')
        footer.note = request.POST.get('note', '')
        
        # Parse links JSON
        links_json_str = request.POST.get('links_json', '[]')
        try:
            footer.links_json = json.loads(links_json_str)
        except:
            footer.links_json = []
        
        footer.save()
        messages.success(request, 'Footer settings updated successfully!')
        return redirect('dashboard:footer_edit')
    
    return render(request, 'dashboard/footer_edit.html', {'footer': footer})


# FAQ Management
@login_required
def faq_section_edit(request):
    """Edit FAQ section configuration"""
    faq_section = FAQSection.objects.first()
    if not faq_section:
        faq_section = FAQSection.objects.create(
            title="Answering your questions",
            description="Still exploring marble suppliers in Dubai or Abu Dhabi?",
            cta_label="Get in touch",
            cta_href="#contact",
            cta_icon="fa-solid fa-arrow-right"
        )
    
    if request.method == 'POST':
        faq_section.title = request.POST.get('title', '')
        faq_section.description = request.POST.get('description', '')
        faq_section.cta_label = request.POST.get('cta_label', '')
        faq_section.cta_href = request.POST.get('cta_href', '')
        faq_section.cta_icon = request.POST.get('cta_icon', '')
        faq_section.save()
        messages.success(request, 'FAQ section updated successfully!')
        return redirect('dashboard:faq_section_edit')
    
    return render(request, 'dashboard/faq_section_edit.html', {'faq_section': faq_section})


@login_required
def faqs_list(request):
    """List all FAQs"""
    faqs = FAQ.objects.all().order_by('sort_order')
    return render(request, 'dashboard/faqs_list.html', {'faqs': faqs})


@login_required
def faq_edit(request, faq_id=None):
    """Create or edit FAQ"""
    if faq_id:
        faq = get_object_or_404(FAQ, id=faq_id)
    else:
        faq = None
    
    if request.method == 'POST':
        if not faq:
            faq = FAQ()
        faq.question = request.POST.get('question', '')
        faq.answer = request.POST.get('answer', '')
        faq.sort_order = int(request.POST.get('sort_order', 0))
        faq.save()
        messages.success(request, f'FAQ {"updated" if faq_id else "created"} successfully!')
        return redirect('dashboard:faqs_list')
    
    return render(request, 'dashboard/faq_edit.html', {'faq': faq})


@login_required
def faq_delete(request, faq_id):
    """Delete FAQ"""
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    messages.success(request, 'FAQ deleted successfully!')
    return redirect('dashboard:faqs_list')


# Testimonials Management
@login_required
def testimonials_list(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all().order_by('sort_order')
    return render(request, 'dashboard/testimonials_list.html', {'testimonials': testimonials})


@login_required
def testimonial_edit(request, testimonial_id=None):
    """Create or edit testimonial"""
    if testimonial_id:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    else:
        testimonial = None
    
    if request.method == 'POST':
        if not testimonial:
            testimonial = Testimonial()
        testimonial.quote = request.POST.get('quote', '')
        testimonial.name = request.POST.get('name', '')
        testimonial.role = request.POST.get('role', '')
        testimonial.avatar = request.POST.get('avatar', '')
        testimonial.sort_order = int(request.POST.get('sort_order', 0))
        testimonial.save()
        messages.success(request, f'Testimonial {"updated" if testimonial_id else "created"} successfully!')
        return redirect('dashboard:testimonials_list')
    
    return render(request, 'dashboard/testimonial_edit.html', {'testimonial': testimonial})


@login_required
def testimonial_delete(request, testimonial_id):
    """Delete testimonial"""
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully!')
    return redirect('dashboard:testimonials_list')


# Promise Section Management
@login_required
def promise_edit(request):
    """Edit Promise section configuration"""
    promise = Promise.objects.first()
    if not promise:
        promise = Promise.objects.create(
            title="Our Promise",
            main_statement="Every surface we touch must look exceptional on day one — and still feel impressive years later.",
            substatement="Clients choose Madrid Marble because we combine technical precision with boutique-level service.",
            closing_statement="We don't just install stone. We engineer statement pieces that hold their value over time."
        )
    
    if request.method == 'POST':
        promise.title = request.POST.get('title', '')
        promise.main_statement = request.POST.get('main_statement', '')
        promise.substatement = request.POST.get('substatement', '')
        promise.closing_statement = request.POST.get('closing_statement', '')
        promise.save()
        messages.success(request, 'Promise section updated successfully!')
        return redirect('dashboard:promise_edit')
    
    return render(request, 'dashboard/promise_edit.html', {'promise': promise})


@login_required
def promise_cards_list(request):
    """List all promise cards"""
    cards = PromiseCard.objects.all().order_by('sort_order')
    return render(request, 'dashboard/promise_cards_list.html', {'cards': cards})


@login_required
def promise_card_edit(request, card_id=None):
    """Create or edit promise card"""
    if card_id:
        card = get_object_or_404(PromiseCard, id=card_id)
    else:
        card = None
    
    if request.method == 'POST':
        if not card:
            card = PromiseCard()
        card.title = request.POST.get('title', '')
        card.description = request.POST.get('description', '')
        card.icon = request.POST.get('icon', '')
        card.sort_order = int(request.POST.get('sort_order', 0))
        card.save()
        messages.success(request, f'Promise card {"updated" if card_id else "created"} successfully!')
        return redirect('dashboard:promise_cards_list')
    
    return render(request, 'dashboard/promise_card_edit.html', {'card': card})


@login_required
def promise_card_delete(request, card_id):
    """Delete promise card"""
    card = get_object_or_404(PromiseCard, id=card_id)
    card.delete()
    messages.success(request, 'Promise card deleted successfully!')
    return redirect('dashboard:promise_cards_list')


# Featured Services Management
@login_required
def featured_services_edit(request):
    """Edit Featured Services section configuration"""
    section = FeaturedServices.objects.first()
    if not section:
        section = FeaturedServices.objects.create(
            title="Featured Services",
            description="From first sketch to final polish, we support your project through every stage — design, fabrication, and installation — with a focus on precision and long-term performance."
        )
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.description = request.POST.get('description', '')
        section.save()
        messages.success(request, 'Featured Services section updated successfully!')
        return redirect('dashboard:featured_services_edit')
    
    return render(request, 'dashboard/featured_services_edit.html', {'section': section})


@login_required
def featured_services_list(request):
    """List all featured services"""
    services = FeaturedService.objects.all().order_by('sort_order')
    return render(request, 'dashboard/featured_services_list.html', {'services': services})


@login_required
def featured_service_edit(request, service_id=None):
    """Create or edit featured service"""
    if service_id:
        service = get_object_or_404(FeaturedService, id=service_id)
    else:
        service = None
    
    if request.method == 'POST':
        if not service:
            service = FeaturedService()
        service.title = request.POST.get('title', '')
        service.description = request.POST.get('description', '')
        service.icon = request.POST.get('icon', '')
        service.sort_order = int(request.POST.get('sort_order', 0))
        service.save()
        messages.success(request, f'Featured service {"updated" if service_id else "created"} successfully!')
        return redirect('dashboard:featured_services_list')
    
    return render(request, 'dashboard/featured_service_edit.html', {'service': service})


@login_required
def featured_service_delete(request, service_id):
    """Delete featured service"""
    service = get_object_or_404(FeaturedService, id=service_id)
    service.delete()
    messages.success(request, 'Featured service deleted successfully!')
    return redirect('dashboard:featured_services_list')


# Why Trust Management
@login_required
def why_trust_edit(request):
    """Edit Why Trust section configuration"""
    section = WhyTrust.objects.first()
    if not section:
        section = WhyTrust.objects.create(
            title="Why Clients Trust Madrid Marble",
            subtitle="We combine the reliability of a specialist contractor with the eye of a design partner."
        )
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.subtitle = request.POST.get('subtitle', '')
        section.save()
        messages.success(request, 'Why Trust section updated successfully!')
        return redirect('dashboard:why_trust_edit')
    
    return render(request, 'dashboard/why_trust_edit.html', {'section': section})


@login_required
def why_trust_factors_list(request):
    """List all why trust factors"""
    factors = WhyTrustFactor.objects.all().order_by('sort_order')
    return render(request, 'dashboard/why_trust_factors_list.html', {'factors': factors})


@login_required
def why_trust_factor_edit(request, factor_id=None):
    """Create or edit why trust factor"""
    if factor_id:
        factor = get_object_or_404(WhyTrustFactor, id=factor_id)
    else:
        factor = None
    
    if request.method == 'POST':
        if not factor:
            factor = WhyTrustFactor()
        factor.title = request.POST.get('title', '')
        factor.description = request.POST.get('description', '')
        factor.icon = request.POST.get('icon', '')
        factor.sort_order = int(request.POST.get('sort_order', 0))
        factor.save()
        messages.success(request, f'Why Trust factor {"updated" if factor_id else "created"} successfully!')
        return redirect('dashboard:why_trust_factors_list')
    
    return render(request, 'dashboard/why_trust_factor_edit.html', {'factor': factor})


@login_required
def why_trust_factor_delete(request, factor_id):
    """Delete why trust factor"""
    factor = get_object_or_404(WhyTrustFactor, id=factor_id)
    factor.delete()
    messages.success(request, 'Why Trust factor deleted successfully!')
    return redirect('dashboard:why_trust_factors_list')


# ==================== INDIVIDUAL PAGES ====================

# About Page
@login_required
def about_page_edit(request):
    """Edit About Page"""
    page = AboutPage.objects.first()
    if not page:
        page = AboutPage.objects.create(
            title="The studio behind the stone.",
            intro_paragraph_1="Madrid Marble was built on a simple belief: every space deserves materials that look as premium as they feel.",
            intro_paragraph_2="What started as a small, highly focused workshop has grown into a trusted marble partner for homeowners, designers, and contractors across the UAE. Over the years, we've invested in better machines, a stronger team, and more refined processes — but our core hasn't changed: deliver precise work, treat every project with respect, and leave clients proud to show their spaces."
        )
    
    if request.method == 'POST':
        page.badge = request.POST.get('badge', '')
        page.title = request.POST.get('title', '')
        page.intro_paragraph_1 = request.POST.get('intro_paragraph_1', '')
        page.intro_paragraph_2 = request.POST.get('intro_paragraph_2', '')
        page.hero_image_url = request.POST.get('hero_image_url', '')
        page.hero_image_alt = request.POST.get('hero_image_alt', '')
        page.since_badge = request.POST.get('since_badge', '')
        page.story_title = request.POST.get('story_title', '')
        page.story_description = request.POST.get('story_description', '')
        page.mission_title = request.POST.get('mission_title', '')
        page.mission_description = request.POST.get('mission_description', '')
        page.sets_apart_title = request.POST.get('sets_apart_title', '')
        page.sets_apart_description = request.POST.get('sets_apart_description', '')
        page.workshop_badge = request.POST.get('workshop_badge', '')
        page.workshop_title = request.POST.get('workshop_title', '')
        page.workshop_description = request.POST.get('workshop_description', '')
        page.workshop_image_url = request.POST.get('workshop_image_url', '')
        page.workshop_image_alt = request.POST.get('workshop_image_alt', '')
        page.values_title = request.POST.get('values_title', '')
        page.values_description = request.POST.get('values_description', '')
        page.team_title = request.POST.get('team_title', '')
        page.team_description = request.POST.get('team_description', '')
        
        # Parse workshop stats JSON
        stats_json_str = request.POST.get('workshop_stats_json', '[]')
        try:
            page.workshop_stats_json = json.loads(stats_json_str)
        except:
            page.workshop_stats_json = []
        
        page.save()
        messages.success(request, 'About Page updated successfully!')
        return redirect('dashboard:about_page_edit')
    
    # Format stats_json for display
    stats_json_str = json.dumps(page.workshop_stats_json, indent=2) if page.workshop_stats_json else '[]'
    
    return render(request, 'dashboard/about_page_edit.html', {
        'page': page,
        'stats_json_str': stats_json_str
    })


@login_required
def about_timeline_list(request):
    """List timeline items"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    timeline_items = page.timeline_items.all().order_by('sort_order')
    return render(request, 'dashboard/about_timeline_list.html', {'timeline_items': timeline_items, 'page': page})


@login_required
def about_timeline_edit(request, item_id=None):
    """Create or edit timeline item"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    
    if item_id:
        item = get_object_or_404(AboutTimelineItem, id=item_id, about_page=page)
    else:
        item = None
    
    if request.method == 'POST':
        if not item:
            item = AboutTimelineItem(about_page=page)
        item.period = request.POST.get('period', '')
        item.description = request.POST.get('description', '')
        item.sort_order = int(request.POST.get('sort_order', 0))
        item.save()
        messages.success(request, f'Timeline item {"updated" if item_id else "created"} successfully!')
        return redirect('dashboard:about_timeline_list')
    
    return render(request, 'dashboard/about_timeline_edit.html', {'item': item, 'page': page})


@login_required
def about_timeline_delete(request, item_id):
    """Delete timeline item"""
    item = get_object_or_404(AboutTimelineItem, id=item_id)
    item.delete()
    messages.success(request, 'Timeline item deleted successfully!')
    return redirect('dashboard:about_timeline_list')


@login_required
def about_mission_cards_list(request):
    """List mission cards"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    cards = page.mission_cards.all().order_by('sort_order')
    return render(request, 'dashboard/about_mission_cards_list.html', {'cards': cards, 'page': page})


@login_required
def about_mission_card_edit(request, card_id=None):
    """Create or edit mission card"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    
    if card_id:
        card = get_object_or_404(AboutMissionCard, id=card_id, about_page=page)
    else:
        card = None
    
    if request.method == 'POST':
        if not card:
            card = AboutMissionCard(about_page=page)
        card.label = request.POST.get('label', '')
        card.description = request.POST.get('description', '')
        card.sort_order = int(request.POST.get('sort_order', 0))
        card.save()
        messages.success(request, f'Mission card {"updated" if card_id else "created"} successfully!')
        return redirect('dashboard:about_mission_cards_list')
    
    return render(request, 'dashboard/about_mission_card_edit.html', {'card': card, 'page': page})


@login_required
def about_mission_card_delete(request, card_id):
    """Delete mission card"""
    card = get_object_or_404(AboutMissionCard, id=card_id)
    card.delete()
    messages.success(request, 'Mission card deleted successfully!')
    return redirect('dashboard:about_mission_cards_list')


@login_required
def about_feature_cards_list(request):
    """List feature cards"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    cards = page.feature_cards.all().order_by('sort_order')
    return render(request, 'dashboard/about_feature_cards_list.html', {'cards': cards, 'page': page})


@login_required
def about_feature_card_edit(request, card_id=None):
    """Create or edit feature card"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    
    if card_id:
        card = get_object_or_404(AboutFeatureCard, id=card_id, about_page=page)
    else:
        card = None
    
    if request.method == 'POST':
        if not card:
            card = AboutFeatureCard(about_page=page)
        card.title = request.POST.get('title', '')
        card.description = request.POST.get('description', '')
        card.icon = request.POST.get('icon', '')
        card.sort_order = int(request.POST.get('sort_order', 0))
        card.save()
        messages.success(request, f'Feature card {"updated" if card_id else "created"} successfully!')
        return redirect('dashboard:about_feature_cards_list')
    
    return render(request, 'dashboard/about_feature_card_edit.html', {'card': card, 'page': page})


@login_required
def about_feature_card_delete(request, card_id):
    """Delete feature card"""
    card = get_object_or_404(AboutFeatureCard, id=card_id)
    card.delete()
    messages.success(request, 'Feature card deleted successfully!')
    return redirect('dashboard:about_feature_cards_list')


@login_required
def about_values_list(request):
    """List values"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    values = page.values.all().order_by('sort_order')
    return render(request, 'dashboard/about_values_list.html', {'values': values, 'page': page})


@login_required
def about_value_edit(request, value_id=None):
    """Create or edit value"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    
    if value_id:
        value = get_object_or_404(AboutValue, id=value_id, about_page=page)
    else:
        value = None
    
    if request.method == 'POST':
        if not value:
            value = AboutValue(about_page=page)
        value.title = request.POST.get('title', '')
        value.description = request.POST.get('description', '')
        value.icon = request.POST.get('icon', '')
        value.sort_order = int(request.POST.get('sort_order', 0))
        value.save()
        messages.success(request, f'Value {"updated" if value_id else "created"} successfully!')
        return redirect('dashboard:about_values_list')
    
    return render(request, 'dashboard/about_value_edit.html', {'value': value, 'page': page})


@login_required
def about_value_delete(request, value_id):
    """Delete value"""
    value = get_object_or_404(AboutValue, id=value_id)
    value.delete()
    messages.success(request, 'Value deleted successfully!')
    return redirect('dashboard:about_values_list')


@login_required
def about_team_members_list(request):
    """List team members"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    members = page.team_members.all().order_by('sort_order')
    return render(request, 'dashboard/about_team_members_list.html', {'members': members, 'page': page})


@login_required
def about_team_member_edit(request, member_id=None):
    """Create or edit team member"""
    page = AboutPage.objects.first()
    if not page:
        return redirect('dashboard:about_page_edit')
    
    if member_id:
        member = get_object_or_404(AboutTeamMember, id=member_id, about_page=page)
    else:
        member = None
    
    if request.method == 'POST':
        if not member:
            member = AboutTeamMember(about_page=page)
        member.name = request.POST.get('name', '')
        member.role = request.POST.get('role', '')
        member.description = request.POST.get('description', '')
        member.avatar_url = request.POST.get('avatar_url', '')
        member.avatar_alt = request.POST.get('avatar_alt', '')
        member.sort_order = int(request.POST.get('sort_order', 0))
        member.save()
        messages.success(request, f'Team member {"updated" if member_id else "created"} successfully!')
        return redirect('dashboard:about_team_members_list')
    
    return render(request, 'dashboard/about_team_member_edit.html', {'member': member, 'page': page})


@login_required
def about_team_member_delete(request, member_id):
    """Delete team member"""
    member = get_object_or_404(AboutTeamMember, id=member_id)
    member.delete()
    messages.success(request, 'Team member deleted successfully!')
    return redirect('dashboard:about_team_members_list')


# Services Page
@login_required
def services_page_edit(request):
    """Edit Services Page"""
    page = ServicesPage.objects.first()
    if not page:
        page = ServicesPage.objects.create(
            title="Full Marble Solutions for Modern Spaces.",
            description="From a single kitchen to full villa interiors and commercial fit-outs, Madrid Marble handles stone selection, technical planning, fabrication, installation, and after-care — all under one specialist team."
        )
    
    if request.method == 'POST':
        page.badge = request.POST.get('badge', '')
        page.title = request.POST.get('title', '')
        page.description = request.POST.get('description', '')
        page.hero_image_1_url = request.POST.get('hero_image_1_url', '')
        page.hero_image_1_alt = request.POST.get('hero_image_1_alt', '')
        page.hero_image_2_url = request.POST.get('hero_image_2_url', '')
        page.hero_image_2_alt = request.POST.get('hero_image_2_alt', '')
        page.hero_image_3_url = request.POST.get('hero_image_3_url', '')
        page.hero_image_3_alt = request.POST.get('hero_image_3_alt', '')
        page.hero_label = request.POST.get('hero_label', '')
        page.solutions_title = request.POST.get('solutions_title', '')
        page.solutions_description = request.POST.get('solutions_description', '')
        page.process_title = request.POST.get('process_title', '')
        page.process_description = request.POST.get('process_description', '')
        page.save()
        messages.success(request, 'Services Page updated successfully!')
        return redirect('dashboard:services_page_edit')
    
    return render(request, 'dashboard/services_page_edit.html', {'page': page})


@login_required
def services_page_services_list(request):
    """List service sections"""
    page = ServicesPage.objects.first()
    if not page:
        return redirect('dashboard:services_page_edit')
    services = page.services.all().order_by('sort_order')
    return render(request, 'dashboard/services_page_services_list.html', {'services': services, 'page': page})


@login_required
def services_page_service_edit(request, service_id=None):
    """Create or edit service section"""
    page = ServicesPage.objects.first()
    if not page:
        return redirect('dashboard:services_page_edit')
    
    if service_id:
        service = get_object_or_404(ServicesPageService, id=service_id, services_page=page)
    else:
        service = None
    
    if request.method == 'POST':
        if not service:
            service = ServicesPageService(services_page=page)
        service.service_id = request.POST.get('service_id', '')
        service.title = request.POST.get('title', '')
        service.description = request.POST.get('description', '')
        service.icon = request.POST.get('icon', '')
        service.image_url = request.POST.get('image_url', '')
        service.image_alt = request.POST.get('image_alt', '')
        service.additional_text = request.POST.get('additional_text', '')
        service.image_position = request.POST.get('image_position', 'right')
        service.sort_order = int(request.POST.get('sort_order', 0))
        
        # Parse features JSON
        features_json_str = request.POST.get('features_json', '[]')
        try:
            service.features_json = json.loads(features_json_str)
        except:
            service.features_json = []
        
        service.save()
        messages.success(request, f'Service section {"updated" if service_id else "created"} successfully!')
        return redirect('dashboard:services_page_services_list')
    
    features_json_str = json.dumps(service.features_json, indent=2) if service and service.features_json else '[]'
    return render(request, 'dashboard/services_page_service_edit.html', {
        'service': service,
        'page': page,
        'features_json_str': features_json_str
    })


@login_required
def services_page_service_delete(request, service_id):
    """Delete service section"""
    service = get_object_or_404(ServicesPageService, id=service_id)
    service.delete()
    messages.success(request, 'Service section deleted successfully!')
    return redirect('dashboard:services_page_services_list')


@login_required
def services_page_process_steps_list(request):
    """List process steps"""
    page = ServicesPage.objects.first()
    if not page:
        return redirect('dashboard:services_page_edit')
    steps = page.process_steps.all().order_by('sort_order')
    return render(request, 'dashboard/services_page_process_steps_list.html', {'steps': steps, 'page': page})


@login_required
def services_page_process_step_edit(request, step_id=None):
    """Create or edit process step"""
    page = ServicesPage.objects.first()
    if not page:
        return redirect('dashboard:services_page_edit')
    
    if step_id:
        step = get_object_or_404(ServicesPageProcessStep, id=step_id, services_page=page)
    else:
        step = None
    
    if request.method == 'POST':
        if not step:
            step = ServicesPageProcessStep(services_page=page)
        step.number = request.POST.get('number', '')
        step.title = request.POST.get('title', '')
        step.description = request.POST.get('description', '')
        step.sort_order = int(request.POST.get('sort_order', 0))
        step.save()
        messages.success(request, f'Process step {"updated" if step_id else "created"} successfully!')
        return redirect('dashboard:services_page_process_steps_list')
    
    return render(request, 'dashboard/services_page_process_step_edit.html', {'step': step, 'page': page})


@login_required
def services_page_process_step_delete(request, step_id):
    """Delete process step"""
    step = get_object_or_404(ServicesPageProcessStep, id=step_id)
    step.delete()
    messages.success(request, 'Process step deleted successfully!')
    return redirect('dashboard:services_page_process_steps_list')


# Portfolio Page
@login_required
def portfolio_page_edit(request):
    """Edit Portfolio Page"""
    page = PortfolioPage.objects.first()
    if not page:
        page = PortfolioPage.objects.create(
            title="Our Masterpieces",
            description="Where timeless elegance meets exceptional craftsmanship. Each project represents our commitment to transforming spaces into works of art."
        )
    
    if request.method == 'POST':
        # Hero Section
        page.hero_badge = request.POST.get('hero_badge', '')
        page.title = request.POST.get('title', '')
        page.description = request.POST.get('description', '')
        page.hero_image_1_url = request.POST.get('hero_image_1_url', '')
        page.hero_image_1_alt = request.POST.get('hero_image_1_alt', '')
        page.hero_image_2_url = request.POST.get('hero_image_2_url', '')
        page.hero_image_2_alt = request.POST.get('hero_image_2_alt', '')
        page.hero_image_3_url = request.POST.get('hero_image_3_url', '')
        page.hero_image_3_alt = request.POST.get('hero_image_3_alt', '')
        
        # Residential Section
        page.residential_badge = request.POST.get('residential_badge', '')
        page.residential_title = request.POST.get('residential_title', '')
        page.residential_description = request.POST.get('residential_description', '')
        page.residential_featured_image_url = request.POST.get('residential_featured_image_url', '')
        page.residential_featured_image_alt = request.POST.get('residential_featured_image_alt', '')
        page.residential_featured_title = request.POST.get('residential_featured_title', '')
        page.residential_featured_description = request.POST.get('residential_featured_description', '')
        
        # Commercial Section
        page.commercial_badge = request.POST.get('commercial_badge', '')
        page.commercial_title = request.POST.get('commercial_title', '')
        page.commercial_description = request.POST.get('commercial_description', '')
        page.commercial_featured_image_url = request.POST.get('commercial_featured_image_url', '')
        page.commercial_featured_image_alt = request.POST.get('commercial_featured_image_alt', '')
        page.commercial_featured_title = request.POST.get('commercial_featured_title', '')
        page.commercial_featured_description = request.POST.get('commercial_featured_description', '')
        
        # CTA Section
        page.cta_title = request.POST.get('cta_title', '')
        page.cta_description = request.POST.get('cta_description', '')
        page.cta_primary_label = request.POST.get('cta_primary_label', '')
        page.cta_primary_href = request.POST.get('cta_primary_href', '/contact/')
        page.cta_secondary_label = request.POST.get('cta_secondary_label', '')
        page.cta_secondary_href = request.POST.get('cta_secondary_href', '/services/')
        
        page.save()
        messages.success(request, 'Portfolio Page updated successfully!')
        return redirect('dashboard:portfolio_page_edit')
    
    return render(request, 'dashboard/portfolio_page_edit.html', {'page': page})


@login_required
def portfolio_page_categories_list(request):
    """List portfolio categories"""
    page = PortfolioPage.objects.first()
    if not page:
        return redirect('dashboard:portfolio_page_edit')
    categories = page.categories.all().order_by('category_type', 'sort_order')
    return render(request, 'dashboard/portfolio_page_categories_list.html', {'categories': categories, 'page': page})


@login_required
def portfolio_page_category_edit(request, category_id=None):
    """Create or edit portfolio category"""
    page = PortfolioPage.objects.first()
    if not page:
        return redirect('dashboard:portfolio_page_edit')
    
    if category_id:
        category = get_object_or_404(PortfolioPageCategory, id=category_id, portfolio_page=page)
    else:
        category = None
    
    if request.method == 'POST':
        if not category:
            category = PortfolioPageCategory(portfolio_page=page)
        category.category_type = request.POST.get('category_type', 'residential')
        category.title = request.POST.get('title', '')
        category.description = request.POST.get('description', '')
        category.icon = request.POST.get('icon', '')
        category.image_url = request.POST.get('image_url', '')
        category.image_alt = request.POST.get('image_alt', '')
        category.sort_order = int(request.POST.get('sort_order', 0))
        category.save()
        messages.success(request, f'Portfolio category {"updated" if category_id else "created"} successfully!')
        return redirect('dashboard:portfolio_page_categories_list')
    
    return render(request, 'dashboard/portfolio_page_category_edit.html', {'category': category, 'page': page})


@login_required
def portfolio_page_category_delete(request, category_id):
    """Delete portfolio category"""
    category = get_object_or_404(PortfolioPageCategory, id=category_id)
    category.delete()
    messages.success(request, 'Portfolio category deleted successfully!')
    return redirect('dashboard:portfolio_page_categories_list')


# FAQ Page
@login_required
def faq_page_edit(request):
    """Edit FAQ Page"""
    page = FAQPage.objects.first()
    if not page:
        page = FAQPage.objects.create(
            title="Questions, answered clearly.",
            description="Here are the questions clients ask us most about timelines, pricing, durability, and warranty — in one place, without the jargon."
        )
    
    if request.method == 'POST':
        page.badge = request.POST.get('badge', '')
        page.title = request.POST.get('title', '')
        page.description = request.POST.get('description', '')
        page.hero_image_url = request.POST.get('hero_image_url', '')
        page.hero_image_alt = request.POST.get('hero_image_alt', '')
        page.hero_label = request.POST.get('hero_label', '')
        page.micro_cta_title = request.POST.get('micro_cta_title', '')
        page.micro_cta_description = request.POST.get('micro_cta_description', '')
        page.final_cta_title = request.POST.get('final_cta_title', '')
        page.final_cta_description = request.POST.get('final_cta_description', '')
        page.final_cta_note_1 = request.POST.get('final_cta_note_1', '')
        page.final_cta_note_2 = request.POST.get('final_cta_note_2', '')
        page.save()
        messages.success(request, 'FAQ Page updated successfully!')
        return redirect('dashboard:faq_page_edit')
    
    return render(request, 'dashboard/faq_page_edit.html', {'page': page})


@login_required
def faq_page_sections_list(request):
    """List FAQ sections"""
    page = FAQPage.objects.first()
    if not page:
        return redirect('dashboard:faq_page_edit')
    sections = page.sections.all().order_by('sort_order')
    return render(request, 'dashboard/faq_page_sections_list.html', {'sections': sections, 'page': page})


@login_required
def faq_page_section_edit(request, section_id=None):
    """Create or edit FAQ section"""
    page = FAQPage.objects.first()
    if not page:
        return redirect('dashboard:faq_page_edit')
    
    if section_id:
        section = get_object_or_404(FAQPageSection, id=section_id, faq_page=page)
    else:
        section = None
    
    if request.method == 'POST':
        if not section:
            section = FAQPageSection(faq_page=page)
        section.section_id = request.POST.get('section_id', '')
        section.title = request.POST.get('title', '')
        section.description = request.POST.get('description', '')
        section.icon = request.POST.get('icon', '')
        section.sort_order = int(request.POST.get('sort_order', 0))
        section.save()
        messages.success(request, f'FAQ section {"updated" if section_id else "created"} successfully!')
        return redirect('dashboard:faq_page_sections_list')
    
    return render(request, 'dashboard/faq_page_section_edit.html', {'section': section, 'page': page})


@login_required
def faq_page_section_delete(request, section_id):
    """Delete FAQ section"""
    section = get_object_or_404(FAQPageSection, id=section_id)
    section.delete()
    messages.success(request, 'FAQ section deleted successfully!')
    return redirect('dashboard:faq_page_sections_list')


@login_required
def faq_page_questions_list(request, section_id):
    """List questions for a FAQ section"""
    section = get_object_or_404(FAQPageSection, id=section_id)
    questions = section.questions.all().order_by('sort_order')
    return render(request, 'dashboard/faq_page_questions_list.html', {'questions': questions, 'section': section})


@login_required
def faq_page_question_edit(request, section_id, question_id=None):
    """Create or edit FAQ question"""
    section = get_object_or_404(FAQPageSection, id=section_id)
    
    if question_id:
        question = get_object_or_404(FAQPageQuestion, id=question_id, faq_section=section)
    else:
        question = None
    
    if request.method == 'POST':
        if not question:
            question = FAQPageQuestion(faq_section=section)
        question.question = request.POST.get('question', '')
        question.answer = request.POST.get('answer', '')
        question.sort_order = int(request.POST.get('sort_order', 0))
        question.save()
        messages.success(request, f'FAQ question {"updated" if question_id else "created"} successfully!')
        return redirect('dashboard:faq_page_questions_list', section_id=section_id)
    
    return render(request, 'dashboard/faq_page_question_edit.html', {'question': question, 'section': section})


@login_required
def faq_page_question_delete(request, question_id):
    """Delete FAQ question"""
    question = get_object_or_404(FAQPageQuestion, id=question_id)
    section_id = question.faq_section.id
    question.delete()
    messages.success(request, 'FAQ question deleted successfully!')
    return redirect('dashboard:faq_page_questions_list', section_id=section_id)


@login_required
def faq_page_tips_list(request, section_id):
    """List tips for a FAQ section"""
    section = get_object_or_404(FAQPageSection, id=section_id)
    tips = section.tips.all().order_by('sort_order')
    return render(request, 'dashboard/faq_page_tips_list.html', {'tips': tips, 'section': section})


@login_required
def faq_page_tip_edit(request, section_id, tip_id=None):
    """Create or edit FAQ tip"""
    section = get_object_or_404(FAQPageSection, id=section_id)
    
    if tip_id:
        tip = get_object_or_404(FAQPageTip, id=tip_id, faq_section=section)
    else:
        tip = None
    
    if request.method == 'POST':
        if not tip:
            tip = FAQPageTip(faq_section=section)
        tip.title = request.POST.get('title', '')
        tip.description = request.POST.get('description', '')
        tip.sort_order = int(request.POST.get('sort_order', 0))
        tip.save()
        messages.success(request, f'FAQ tip {"updated" if tip_id else "created"} successfully!')
        return redirect('dashboard:faq_page_tips_list', section_id=section_id)
    
    return render(request, 'dashboard/faq_page_tip_edit.html', {'tip': tip, 'section': section})


@login_required
def faq_page_tip_delete(request, tip_id):
    """Delete FAQ tip"""
    tip = get_object_or_404(FAQPageTip, id=tip_id)
    section_id = tip.faq_section.id
    tip.delete()
    messages.success(request, 'FAQ tip deleted successfully!')
    return redirect('dashboard:faq_page_tips_list', section_id=section_id)


# Contact Page
@login_required
def contact_page_edit(request):
    """Edit Contact Page"""
    page = ContactPage.objects.first()
    if not page:
        page = ContactPage.objects.create(
            title="Let's turn your ideas into solid marble reality.",
            description="Share your drawings, inspiration photos, or even a rough concept — our team will help you refine it into a buildable plan with the right stone, finish, and budget."
        )
    
    if request.method == 'POST':
        page.badge = request.POST.get('badge', '')
        page.title = request.POST.get('title', '')
        page.description = request.POST.get('description', '')
        page.hero_feature_1_text = request.POST.get('hero_feature_1_text', '')
        page.hero_feature_2_text = request.POST.get('hero_feature_2_text', '')
        page.hero_background_image_url = request.POST.get('hero_background_image_url', '')
        page.contact_details_title = request.POST.get('contact_details_title', '')
        page.contact_details_description = request.POST.get('contact_details_description', '')
        page.business_hours_title = request.POST.get('business_hours_title', '')
        page.business_hours_description = request.POST.get('business_hours_description', '')
        
        # Parse business hours JSON
        hours_json_str = request.POST.get('business_hours_json', '[]')
        try:
            page.business_hours_json = json.loads(hours_json_str)
        except:
            page.business_hours_json = []
        
        page.save()
        messages.success(request, 'Contact Page updated successfully!')
        return redirect('dashboard:contact_page_edit')
    
    hours_json_str = json.dumps(page.business_hours_json, indent=2) if page.business_hours_json else '[]'
    return render(request, 'dashboard/contact_page_edit.html', {
        'page': page,
        'hours_json_str': hours_json_str
    })

