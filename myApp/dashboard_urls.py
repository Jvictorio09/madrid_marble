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
    
    # Promise Section
    path('promise/', dashboard_views.promise_edit, name='promise_edit'),
    path('promise/cards/', dashboard_views.promise_cards_list, name='promise_cards_list'),
    path('promise/cards/add/', dashboard_views.promise_card_edit, name='promise_card_add'),
    path('promise/cards/<int:card_id>/edit/', dashboard_views.promise_card_edit, name='promise_card_edit'),
    path('promise/cards/<int:card_id>/delete/', dashboard_views.promise_card_delete, name='promise_card_delete'),
    
    # Featured Services
    path('featured-services/', dashboard_views.featured_services_edit, name='featured_services_edit'),
    path('featured-services/items/', dashboard_views.featured_services_list, name='featured_services_list'),
    path('featured-services/items/add/', dashboard_views.featured_service_edit, name='featured_service_add'),
    path('featured-services/items/<int:service_id>/edit/', dashboard_views.featured_service_edit, name='featured_service_edit'),
    path('featured-services/items/<int:service_id>/delete/', dashboard_views.featured_service_delete, name='featured_service_delete'),
    
    # Why Trust
    path('why-trust/', dashboard_views.why_trust_edit, name='why_trust_edit'),
    path('why-trust/factors/', dashboard_views.why_trust_factors_list, name='why_trust_factors_list'),
    path('why-trust/factors/add/', dashboard_views.why_trust_factor_edit, name='why_trust_factor_add'),
    path('why-trust/factors/<int:factor_id>/edit/', dashboard_views.why_trust_factor_edit, name='why_trust_factor_edit'),
    path('why-trust/factors/<int:factor_id>/delete/', dashboard_views.why_trust_factor_delete, name='why_trust_factor_delete'),
    
    # Individual Pages - About Page
    path('pages/about/', dashboard_views.about_page_edit, name='about_page_edit'),
    path('pages/about/timeline/', dashboard_views.about_timeline_list, name='about_timeline_list'),
    path('pages/about/timeline/add/', dashboard_views.about_timeline_edit, name='about_timeline_add'),
    path('pages/about/timeline/<int:item_id>/edit/', dashboard_views.about_timeline_edit, name='about_timeline_edit'),
    path('pages/about/timeline/<int:item_id>/delete/', dashboard_views.about_timeline_delete, name='about_timeline_delete'),
    path('pages/about/mission-cards/', dashboard_views.about_mission_cards_list, name='about_mission_cards_list'),
    path('pages/about/mission-cards/add/', dashboard_views.about_mission_card_edit, name='about_mission_card_add'),
    path('pages/about/mission-cards/<int:card_id>/edit/', dashboard_views.about_mission_card_edit, name='about_mission_card_edit'),
    path('pages/about/mission-cards/<int:card_id>/delete/', dashboard_views.about_mission_card_delete, name='about_mission_card_delete'),
    path('pages/about/feature-cards/', dashboard_views.about_feature_cards_list, name='about_feature_cards_list'),
    path('pages/about/feature-cards/add/', dashboard_views.about_feature_card_edit, name='about_feature_card_add'),
    path('pages/about/feature-cards/<int:card_id>/edit/', dashboard_views.about_feature_card_edit, name='about_feature_card_edit'),
    path('pages/about/feature-cards/<int:card_id>/delete/', dashboard_views.about_feature_card_delete, name='about_feature_card_delete'),
    path('pages/about/values/', dashboard_views.about_values_list, name='about_values_list'),
    path('pages/about/values/add/', dashboard_views.about_value_edit, name='about_value_add'),
    path('pages/about/values/<int:value_id>/edit/', dashboard_views.about_value_edit, name='about_value_edit'),
    path('pages/about/values/<int:value_id>/delete/', dashboard_views.about_value_delete, name='about_value_delete'),
    path('pages/about/team/', dashboard_views.about_team_members_list, name='about_team_members_list'),
    path('pages/about/team/add/', dashboard_views.about_team_member_edit, name='about_team_member_add'),
    path('pages/about/team/<int:member_id>/edit/', dashboard_views.about_team_member_edit, name='about_team_member_edit'),
    path('pages/about/team/<int:member_id>/delete/', dashboard_views.about_team_member_delete, name='about_team_member_delete'),
    
    # Individual Pages - Services Page
    path('pages/services/', dashboard_views.services_page_edit, name='services_page_edit'),
    path('pages/services/service-sections/', dashboard_views.services_page_services_list, name='services_page_services_list'),
    path('pages/services/service-sections/add/', dashboard_views.services_page_service_edit, name='services_page_service_add'),
    path('pages/services/service-sections/<int:service_id>/edit/', dashboard_views.services_page_service_edit, name='services_page_service_edit'),
    path('pages/services/service-sections/<int:service_id>/delete/', dashboard_views.services_page_service_delete, name='services_page_service_delete'),
    path('pages/services/process-steps/', dashboard_views.services_page_process_steps_list, name='services_page_process_steps_list'),
    path('pages/services/process-steps/add/', dashboard_views.services_page_process_step_edit, name='services_page_process_step_add'),
    path('pages/services/process-steps/<int:step_id>/edit/', dashboard_views.services_page_process_step_edit, name='services_page_process_step_edit'),
    path('pages/services/process-steps/<int:step_id>/delete/', dashboard_views.services_page_process_step_delete, name='services_page_process_step_delete'),
    
    # Individual Pages - Portfolio Page
    path('pages/portfolio/', dashboard_views.portfolio_page_edit, name='portfolio_page_edit'),
    path('pages/portfolio/categories/', dashboard_views.portfolio_page_categories_list, name='portfolio_page_categories_list'),
    path('pages/portfolio/categories/add/', dashboard_views.portfolio_page_category_edit, name='portfolio_page_category_add'),
    path('pages/portfolio/categories/<int:category_id>/edit/', dashboard_views.portfolio_page_category_edit, name='portfolio_page_category_edit'),
    path('pages/portfolio/categories/<int:category_id>/delete/', dashboard_views.portfolio_page_category_delete, name='portfolio_page_category_delete'),
    
    # Individual Pages - FAQ Page
    path('pages/faq/', dashboard_views.faq_page_edit, name='faq_page_edit'),
    path('pages/faq/sections/', dashboard_views.faq_page_sections_list, name='faq_page_sections_list'),
    path('pages/faq/sections/add/', dashboard_views.faq_page_section_edit, name='faq_page_section_add'),
    path('pages/faq/sections/<int:section_id>/edit/', dashboard_views.faq_page_section_edit, name='faq_page_section_edit'),
    path('pages/faq/sections/<int:section_id>/delete/', dashboard_views.faq_page_section_delete, name='faq_page_section_delete'),
    path('pages/faq/sections/<int:section_id>/questions/', dashboard_views.faq_page_questions_list, name='faq_page_questions_list'),
    path('pages/faq/sections/<int:section_id>/questions/add/', dashboard_views.faq_page_question_edit, name='faq_page_question_add'),
    path('pages/faq/sections/<int:section_id>/questions/<int:question_id>/edit/', dashboard_views.faq_page_question_edit, name='faq_page_question_edit'),
    path('pages/faq/sections/<int:section_id>/questions/<int:question_id>/delete/', dashboard_views.faq_page_question_delete, name='faq_page_question_delete'),
    path('pages/faq/sections/<int:section_id>/tips/', dashboard_views.faq_page_tips_list, name='faq_page_tips_list'),
    path('pages/faq/sections/<int:section_id>/tips/add/', dashboard_views.faq_page_tip_edit, name='faq_page_tip_add'),
    path('pages/faq/sections/<int:section_id>/tips/<int:tip_id>/edit/', dashboard_views.faq_page_tip_edit, name='faq_page_tip_edit'),
    path('pages/faq/sections/<int:section_id>/tips/<int:tip_id>/delete/', dashboard_views.faq_page_tip_delete, name='faq_page_tip_delete'),
    
    # Individual Pages - Contact Page
    path('pages/contact/', dashboard_views.contact_page_edit, name='contact_page_edit'),
]

