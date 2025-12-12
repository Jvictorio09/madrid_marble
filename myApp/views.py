from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
import json
import requests
import time
import logging
from typing import Iterable, Mapping, Any

from .content.homepage import get_homepage_content
from .content_helpers import get_homepage_content_from_db
from django.conf import settings

logger = logging.getLogger(__name__)


def get_content():
    """Helper function to get content from database or JSON fallback"""
    try:
        # Try to get content from database
        return get_homepage_content_from_db()
    except:
        # Fall back to JSON file if database is not set up
        return get_homepage_content()


def home(request):
    """Homepage view - uses database if available, falls back to JSON"""
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "home.html", context)


def about(request):
    """About page view"""
    from .models import AboutPage
    
    content = get_content()
    about_page = AboutPage.objects.first()
    
    context = {
        "content": content,
        "about_page": about_page
    }
    return render(request, "about.html", context)


def services(request):
    """Services page view"""
    from .models import ServicesPage
    
    content = get_content()
    services_page = ServicesPage.objects.first()
    
    context = {
        "content": content,
        "services_page": services_page
    }
    return render(request, "services.html", context)


def portfolio(request):
    """Portfolio page view"""
    from .models import PortfolioPage
    
    content = get_content()
    portfolio_page = PortfolioPage.objects.first()
    
    context = {
        "content": content,
        "portfolio_page": portfolio_page
    }
    return render(request, "portfolio.html", context)


def faq(request):
    """FAQ page view"""
    from .models import FAQPage
    
    content = get_content()
    faq_page = FAQPage.objects.first()
    
    context = {
        "content": content,
        "faq_page": faq_page
    }
    return render(request, "faq.html", context)


def contact(request):
    """Contact page view"""
    from .models import ContactPage
    
    content = get_content()
    contact_page = ContactPage.objects.first()
    
    context = {
        "content": content,
        "contact_page": contact_page
    }
    return render(request, "contact.html", context)


def privacy_policy(request):
    """Privacy Policy page view"""
    content = get_content()
    context = {
        "content": content
    }
    return render(request, "privacy_policy.html", context)


def send_email_resend(
    *,
    subject: str,
    to: Iterable[str],
    text: str,
    html: str,
    reply_to: str | None = None,
    tags: Mapping[str, Any] | None = None,
) -> tuple[bool, str]:
    """
    Send an email with Resend (https://resend.com).
    Returns (ok, message_or_error).
    """
    api_key = getattr(settings, "RESEND_API_KEY", None)
    sender = getattr(settings, "RESEND_FROM", getattr(settings, "DEFAULT_FROM_EMAIL", None))
    base_url = getattr(settings, "RESEND_BASE_URL", "https://api.resend.com")

    if not api_key or not sender:
        return (False, "Resend not configured: missing RESEND_API_KEY or RESEND_FROM.")

    url = f"{base_url.rstrip('/')}/emails"
    payload = {
        "from": sender,
        "to": list(to),
        "subject": subject[:300],  # keep it reasonable
        "text": text,
        "html": html,
    }
    if reply_to:
        payload["reply_to"] = [reply_to]
    if tags:
        # Resend supports custom headers/metadata via tags
        payload["tags"] = [{"name": str(k), "value": str(v)} for k, v in tags.items()]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if resp.status_code in (200, 201, 202):
            return (True, "Sent")
        # Try to surface JSON error if present
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        logger.error("Resend error %s: %s", resp.status_code, detail)
        return (False, f"Resend error {resp.status_code}: {detail}")
    except requests.RequestException as e:
        logger.exception("Resend request failed")
        return (False, f"Resend request failed: {e}")


@csrf_exempt  # Public API endpoint - consider adding rate limiting in production
@require_http_methods(["POST"])
def contact_submit(request):
    """Handle contact form submission and send emails via Resend"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    
    # Validate required fields
    required_fields = ["name", "email"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return JsonResponse({
            "success": False,
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }, status=400)
    
    # Validate privacy consent
    privacy_consent = data.get("privacy_consent", False)
    if not privacy_consent:
        return JsonResponse({
            "success": False,
            "error": "You must agree to the privacy policy to submit the form."
        }, status=400)
    
    # Extract form data
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    project_type = data.get("project_type", "").strip()
    project_location = data.get("project_location", "").strip()
    message = data.get("project_details", "").strip()  # Form uses "project_details" field name
    
    # Validate email format
    if email and "@" not in email:
        return JsonResponse({
            "success": False,
            "error": "Invalid email address"
        }, status=400)
    
    # Always send team notifications to info@madridmarble.com
    team_email = "info@madridmarble.com"
    
    # Build notification email to team
    service = project_type or "General Inquiry"
    location = project_location or "Not specified"
    
    subject = f"New Contact Form Submission - {service}"
    
    # Build team notification text
    text_parts = [
        f"New contact form submission from {name}",
        "",
        "Contact Details:",
        f"Name: {name}",
        f"Email: {email}",
    ]
    if phone:
        text_parts.append(f"Phone: {phone}")
    text_parts.extend([
        "",
        "Project Details:",
        f"Project Type: {service}",
        f"Location: {location}",
    ])
    if message:
        text_parts.extend([
            "",
            "Message:",
            message,
        ])
    text = "\n".join(text_parts)
    
    # Build team notification HTML
    html_parts = [
        "<div style='font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:600px;margin:0 auto;'>",
        f"<h2 style='color:#1a1a1a;margin-bottom:20px;'>New Contact Form Submission</h2>",
        f"<p><strong>From:</strong> {escape(name)}</p>",
        f"<p><strong>Email:</strong> <a href='mailto:{escape(email)}'>{escape(email)}</a></p>",
    ]
    if phone:
        html_parts.append(f"<p><strong>Phone:</strong> {escape(phone)}</p>")
    html_parts.extend([
        "<div style='background-color:#f9fafb;border-left:4px solid #1a1a1a;padding:16px;margin:20px 0;'>",
        "<h3 style='margin:0 0 12px 0;color:#1a1a1a;font-size:16px;'>Project Details:</h3>",
        f"<p style='margin:4px 0;'><strong>Project Type:</strong> {escape(service)}</p>",
        f"<p style='margin:4px 0;'><strong>Location:</strong> {escape(location)}</p>",
    ])
    if message:
        html_parts.append(f"<p style='margin:4px 0;'><strong>Message:</strong> {escape(message)}</p>")
    html_parts.extend([
        "</div>",
        f"<p><a href='mailto:{escape(email)}' style='color:#1a1a1a;text-decoration:underline;'>Reply to {escape(name)}</a></p>",
        "</div>",
    ])
    html = "".join(html_parts)
    
    # Send notification email to team at info@madridmarble.com
    logger.info(f"Sending contact form notification to {team_email} from {email}")
    ok, detail = send_email_resend(
        subject=subject,
        to=[team_email],
        text=text,
        html=html,
        reply_to=email,  # Reply-to is the user's email so team can reply directly
        tags={"env": getattr(settings, "ENVIRONMENT", "prod"), "type": "contact"},
    )
    
    if not ok:
        logger.error(f"Failed to send contact notification email to {team_email}: {detail}")
        return JsonResponse({
            "success": False,
            "error": "Failed to send email. Please try again later."
        }, status=500)
    
    logger.info(f"Successfully sent contact notification email to {team_email}")
    
    # Add delay to avoid Resend rate limit (2 requests/second)
    time.sleep(0.6)
    
    # Send auto-response to user
    auto_response_subject = f"Thank you for your inquiry - {service}"
    
    # Build user-facing text
    user_text_parts = [
        f"Dear {name},",
        "",
        f"Thank you for submitting your inquiry for {service}",
    ]
    if location and location != "Not specified":
        user_text_parts[-1] += f" in {location}"
    user_text_parts[-1] += "."
    
    user_text_parts.extend([
        "",
        "Your request details:",
        f"- Project Type: {service}",
    ])
    if location and location != "Not specified":
        user_text_parts.append(f"- Location: {location}")
    if message:
        user_text_parts.extend([
            f"- Message: {message[:100]}{'...' if len(message) > 100 else ''}",
        ])
    
    user_text_parts.extend([
        "",
        "We have received your request and will review it shortly. Our team will contact you within 24-48 hours to discuss your project requirements and provide you with a detailed quote.",
        "",
        "If you have any urgent questions, please don't hesitate to contact us directly.",
        "",
        "Best regards,",
        "The Madrid Marble Team",
    ])
    user_text = "\n".join(user_text_parts)
    
    # Build HTML version
    user_html_parts = [
        "<div style='font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:600px;margin:0 auto;'>",
        f"<p>Dear {escape(name)},</p>",
        f"<p>Thank you for submitting your inquiry for <strong>{escape(service)}</strong>",
    ]
    if location and location != "Not specified":
        user_html_parts[-1] += f" in <strong>{escape(location)}</strong>"
    user_html_parts[-1] += ".</p>"
    
    user_html_parts.extend([
        "<div style='background-color:#f9fafb;border-left:4px solid #1a1a1a;padding:16px;margin:20px 0;'>",
        "<h3 style='margin:0 0 12px 0;color:#1a1a1a;font-size:16px;'>Your request details:</h3>",
        f"<p style='margin:4px 0;'><strong>Project Type:</strong> {escape(service)}</p>",
    ])
    if location and location != "Not specified":
        user_html_parts.append(f"<p style='margin:4px 0;'><strong>Location:</strong> {escape(location)}</p>")
    if message:
        user_html_parts.append(f"<p style='margin:4px 0;'><strong>Message:</strong> {escape(message[:150])}{'...' if len(message) > 150 else ''}</p>")
    
    user_html_parts.extend([
        "</div>",
        "<p>We have received your request and will review it shortly. <strong>Our team will contact you within 24-48 hours</strong> to discuss your project requirements and provide you with a detailed quote.</p>",
        "<p>If you have any urgent questions, please don't hesitate to contact us directly.</p>",
        "<p style='margin-top:30px;'>Best regards,<br><strong style='color:#1a1a1a;'>The Madrid Marble Team</strong></p>",
        "</div>",
    ])
    user_html = "".join(user_html_parts)
    
    # Send auto-response to user (don't fail if this doesn't work)
    try:
        logger.info(f"Sending auto-response email to {email}")
        auto_ok, auto_detail = send_email_resend(
            subject=auto_response_subject,
            to=[email],  # Send to the user's email
            text=user_text,
            html=user_html,
            reply_to=team_email,  # Reply-to is info@madridmarble.com so user can reply
            tags={"env": getattr(settings, "ENVIRONMENT", "prod"), "type": "auto_response"},
        )
        if not auto_ok:
            logger.warning(f"Failed to send auto-response email to {email}: {auto_detail}")
        else:
            logger.info(f"Successfully sent auto-response email to {email}")
    except Exception as e:
        logger.error(f"Exception sending auto-response email to {email}: {e}")
    
    return JsonResponse({
        "success": True,
        "message": "Thank you for your inquiry! We'll get back to you within 24-48 hours."
    })
