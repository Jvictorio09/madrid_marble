from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from . import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='dashboard/login.html',
        authentication_form=AuthenticationForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard Home
    path('', dashboard_views.dashboard_home, name='home'),
    
    # Image Upload & Gallery
    path('gallery/', dashboard_views.gallery, name='gallery'),
    path('upload-image/', dashboard_views.upload_image, name='upload_image'),
    
    # SEO
    path('seo/', dashboard_views.seo_edit, name='seo_edit'),
    
    # Navigation
    path('navigation/', dashboard_views.navigation_edit, name='navigation_edit'),
    
    # Hero
    path('hero/', dashboard_views.hero_edit, name='hero_edit'),
    
    # About
    path('about/', dashboard_views.about_edit, name='about_edit'),
    
    # Stats
    path('stats/', dashboard_views.stats_list, name='stats_list'),
    path('stats/add/', dashboard_views.stat_edit, name='stat_add'),
    path('stats/<int:stat_id>/edit/', dashboard_views.stat_edit, name='stat_edit'),
    path('stats/<int:stat_id>/delete/', dashboard_views.stat_delete, name='stat_delete'),
    
    # Services
    path('services/section/', dashboard_views.services_section_edit, name='services_section_edit'),
    path('services/', dashboard_views.services_list, name='services_list'),
    path('services/add/', dashboard_views.service_edit, name='service_add'),
    path('services/<int:service_id>/edit/', dashboard_views.service_edit, name='service_edit'),
    path('services/<int:service_id>/delete/', dashboard_views.service_delete, name='service_delete'),
    
    # Portfolio
    path('portfolio/', dashboard_views.portfolio_edit, name='portfolio_edit'),
    path('portfolio/projects/', dashboard_views.portfolio_projects_list, name='portfolio_projects_list'),
    path('portfolio/projects/add/', dashboard_views.portfolio_project_edit, name='portfolio_project_add'),
    path('portfolio/projects/<int:project_id>/edit/', dashboard_views.portfolio_project_edit, name='portfolio_project_edit'),
    path('portfolio/projects/<int:project_id>/toggle/', dashboard_views.portfolio_project_toggle_active, name='portfolio_project_toggle'),
    path('portfolio/projects/<int:project_id>/delete/', dashboard_views.portfolio_project_delete, name='portfolio_project_delete'),
    
    # Contact
    path('contact/', dashboard_views.contact_edit, name='contact_edit'),
    path('contact/info/', dashboard_views.contact_info_list, name='contact_info_list'),
    path('contact/info/add/', dashboard_views.contact_info_edit, name='contact_info_add'),
    path('contact/info/<int:info_id>/edit/', dashboard_views.contact_info_edit, name='contact_info_edit'),
    path('contact/info/<int:info_id>/delete/', dashboard_views.contact_info_delete, name='contact_info_delete'),
    path('contact/fields/', dashboard_views.contact_form_fields_list, name='contact_form_fields_list'),
    path('contact/fields/add/', dashboard_views.contact_form_field_edit, name='contact_form_field_add'),
    path('contact/fields/<int:field_id>/edit/', dashboard_views.contact_form_field_edit, name='contact_form_field_edit'),
    path('contact/fields/<int:field_id>/delete/', dashboard_views.contact_form_field_delete, name='contact_form_field_delete'),
    path('contact/social/', dashboard_views.social_links_list, name='social_links_list'),
    path('contact/social/add/', dashboard_views.social_link_edit, name='social_link_add'),
    path('contact/social/<int:link_id>/edit/', dashboard_views.social_link_edit, name='social_link_edit'),
    path('contact/social/<int:link_id>/delete/', dashboard_views.social_link_delete, name='social_link_delete'),
    
    # Footer
    path('footer/', dashboard_views.footer_edit, name='footer_edit'),
    
    # FAQ
    path('faq/section/', dashboard_views.faq_section_edit, name='faq_section_edit'),
    path('faq/', dashboard_views.faqs_list, name='faqs_list'),
    path('faq/add/', dashboard_views.faq_edit, name='faq_add'),
    path('faq/<int:faq_id>/edit/', dashboard_views.faq_edit, name='faq_edit'),
    path('faq/<int:faq_id>/delete/', dashboard_views.faq_delete, name='faq_delete'),
    
    # Testimonials
    path('testimonials/', dashboard_views.testimonials_list, name='testimonials_list'),
    path('testimonials/add/', dashboard_views.testimonial_edit, name='testimonial_add'),
    path('testimonials/<int:testimonial_id>/edit/', dashboard_views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/<int:testimonial_id>/delete/', dashboard_views.testimonial_delete, name='testimonial_delete'),
]

