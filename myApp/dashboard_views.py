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
    Contact, ContactInfo, ContactFormField, SocialLink, Footer, MediaAsset
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
        hero.save()
        messages.success(request, 'Hero section updated successfully!')
        return redirect('dashboard:hero_edit')
    
    return render(request, 'dashboard/hero_edit.html', {'hero': hero})


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
        copy_json_str = request.POST.get('copy_json', '[]')
        try:
            about.copy_json = json.loads(copy_json_str)
        except:
            about.copy_json = []
        
        # Parse gallery JSON
        gallery_json_str = request.POST.get('gallery_json', '[]')
        try:
            about.gallery_json = json.loads(gallery_json_str)
        except:
            about.gallery_json = []
        
        about.save()
        messages.success(request, 'About section updated successfully!')
        return redirect('dashboard:about_edit')
    
    # Convert gallery_json to JSON string for template
    import json as json_lib
    gallery_json_str = json_lib.dumps(about.gallery_json) if about.gallery_json else '[]'
    
    return render(request, 'dashboard/about_edit.html', {
        'about': about,
        'gallery_json_str': gallery_json_str
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

