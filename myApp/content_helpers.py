"""
Helper functions to convert database models to JSON format for templates
"""
from .models import (
    SEO, Navigation, Hero, About, Stat, Service, Services,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer
)


def get_homepage_content_from_db():
    """Convert database models to JSON format for templates"""
    
    # Get or create default instances
    seo = SEO.objects.first()
    nav = Navigation.objects.first()
    hero = Hero.objects.first()
    about = About.objects.first()
    stats = Stat.objects.all().order_by('sort_order')
    services_section = Services.objects.first()
    services = Service.objects.all().order_by('sort_order')
    portfolio = Portfolio.objects.first()
    portfolio_projects = PortfolioProject.objects.all().order_by('sort_order')
    testimonials = Testimonial.objects.all().order_by('sort_order')
    faq_section = FAQSection.objects.first()
    faqs = FAQ.objects.all().order_by('sort_order')
    contact = Contact.objects.first()
    contact_info = ContactInfo.objects.all().order_by('sort_order')
    contact_form_fields = ContactFormField.objects.filter(contact=contact).order_by('sort_order') if contact else []
    social_links = SocialLink.objects.all().order_by('sort_order')
    footer = Footer.objects.first()
    
    # Build content dictionary
    content = {
        "seo": {
            "title": seo.title if seo else "",
            "description": seo.description if seo else "",
            "canonical": seo.canonical if seo else "",
            "og": {
                "title": seo.og_title if seo else "",
                "description": seo.og_description if seo else "",
                "image": seo.og_image if seo else "",
            },
            "favicon": seo.favicon if seo else "",
            "preload_hero": seo.preload_hero if seo else "",
        },
        "nav": {
            "logo_text": nav.logo_text if nav else "MM",
            "logo_image_url": nav.logo_image_url if nav else "",
            "brand": nav.brand if nav else "Madrid Marble",
            "links": nav.links_json if nav else [],
            "cta": {
                "label": nav.cta_label if nav else "",
                "href": nav.cta_href if nav else "#contact",
            }
        },
        "hero": {
            "badge": hero.badge if hero else "",
            "headline": hero.headline if hero else "",
            "description": hero.description if hero else "",
            "primary_cta": {
                "label": hero.primary_cta_label if hero else "",
                "href": hero.primary_cta_href if hero else "#contact",
                "icon": hero.primary_cta_icon if hero else "",
            },
            "secondary_cta": {
                "label": hero.secondary_cta_label if hero else "",
                "href": hero.secondary_cta_href if hero else "",
            },
            "image": {
                "url": hero.image_url if hero else "",
                "alt": hero.image_alt if hero else "",
            },
            "testimonial": {
                "quote": hero.testimonial_quote if hero else "",
                "name": hero.testimonial_name if hero else "",
                "meta": hero.testimonial_meta if hero else "",
                "stars": hero.testimonial_stars if hero else 5,
            }
        },
        "about": {
            "badge": about.badge if about else "",
            "title": about.title if about else "",
            "copy": about.copy_json if about else [],
            "gallery": about.gallery_json if about else [],
        },
        "stats": [
            {
                "value": stat.value,
                "label": stat.label,
                "description": stat.description,
            }
            for stat in stats
        ],
        "services": {
            "title": services_section.title if services_section else "",
            "description": services_section.description if services_section else "",
            "image": {
                "url": services_section.image_url if services_section else "",
                "alt": services_section.image_alt if services_section else "",
            },
            "items": [
                {
                    "title": service.title,
                    "description": service.description,
                    "icon": service.icon,
                    "open": service.is_open,
                }
                for service in services
            ]
        },
        "portfolio": {
            "heading": portfolio.heading if portfolio else "",
            "description": portfolio.description if portfolio else "",
            "feature": {
                "image": {
                    "url": portfolio.feature_image_url if portfolio else "",
                    "alt": portfolio.feature_image_alt if portfolio else "",
                },
                "title": portfolio.feature_title if portfolio else "",
                "description": portfolio.feature_description if portfolio else "",
                "tags": portfolio.feature_tags_json if portfolio else [],
                "testimonial": {
                    "quote": portfolio.feature_testimonial_quote if portfolio else "",
                    "author": portfolio.feature_testimonial_author if portfolio else "",
                },
                "cta": {
                    "label": portfolio.feature_cta_label if portfolio else "",
                    "href": portfolio.feature_cta_href if portfolio else "#contact",
                    "icon": portfolio.feature_cta_icon if portfolio else "",
                }
            },
            "projects": [
                {
                    "image": {
                        "url": project.image_url,
                        "alt": project.image_alt,
                    },
                    "title": project.title,
                    "description": project.description,
                }
                for project in portfolio_projects.filter(is_active=True)
            ]
        },
        "testimonials": [
            {
                "quote": testimonial.quote,
                "name": testimonial.name,
                "role": testimonial.role,
                "avatar": testimonial.avatar,
            }
            for testimonial in testimonials
        ],
        "faq": {
            "title": faq_section.title if faq_section else "",
            "description": faq_section.description if faq_section else "",
            "cta": {
                "label": faq_section.cta_label if faq_section else "",
                "href": faq_section.cta_href if faq_section else "#contact",
                "icon": faq_section.cta_icon if faq_section else "",
            },
            "items": [
                {
                    "question": faq.question,
                    "answer": faq.answer,
                }
                for faq in faqs
            ]
        },
        "contact": {
            "badge": contact.badge if contact else "CONTACT",
            "heading": contact.heading if contact else "",
            "description": contact.description if contact else "",
            "intro_text": contact.intro_text if contact else "",
            "background_image": contact.background_image if contact else "",
            "info": [
                {
                    "label": info.label,
                    "text": info.text,
                    "href": info.href,
                    "type": info.info_type,
                }
                for info in contact_info
            ],
            "socials": {
                "label": contact.socials_label if contact else "FOLLOW MADRID MARBLE",
                "links": [
                    {
                        "icon": link.icon,
                        "href": link.href,
                    }
                    for link in social_links
                ]
            },
            "form": {
                "fields": [
                    {
                        "name": field.name,
                        "label": field.label,
                        "type": field.field_type,
                        "placeholder": field.placeholder,
                        "span": field.span,
                        "rows": field.rows,
                        "required": field.required,
                    }
                    for field in contact_form_fields
                ],
                "submit": {
                    "label": contact.form_submit_label if contact else "Submit inquiry",
                },
                "disclaimer": contact.form_disclaimer if contact else "",
            }
        },
        "footer": {
            "logo_text": footer.logo_text if footer else "MM",
            "note": footer.note if footer else "Madrid Marble. All rights reserved.",
            "links": footer.links_json if footer else [],
        }
    }
    
    return content


