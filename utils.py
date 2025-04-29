"""Utility functions for the internship email sender tool."""

import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from email.utils import formataddr


def load_template(language):
    """Load email template from file based on language"""
    template_path = Path(f"templates/email_{language}.txt")
    if not template_path.exists():
        print(f"Error: Template file {template_path} not found.")
        return None

    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading template {template_path}: {e}")
        return None


def generate_email_body(company_name, country, language, responsible_name=None, is_debug=False):
    """Generate email body using a template with simple replacements"""
    print(f"\n🔍 Preparing email for: {company_name} ({country})")

    language = language.lower() if language in ["en", "fr"] else "en"
    if is_debug:
        print(f"🌐 Selected language: {language.upper()}")

    template = load_template(language)
    if not template:
        return None, None

    responsible = responsible_name or ("Hiring Manager" if language == "en" else "Madame, Monsieur")

    email_body = template.replace("{{COMPANY_NAME}}", company_name)
    email_body = email_body.replace("{{RESPONSIBLE_NAME}}", responsible)
    
    return language, email_body


def create_email(recipient_email, body, language, sender_name, sender_email,
                 signature_path, cv_en_path, cv_fr_path, is_debug=False):
    """Create email with inline signature and CV attachment"""
    msg = MIMEMultipart('related')
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = recipient_email
    msg['Subject'] = ("Candidature pour un stage d'été" if language == "fr" else "Application for Summer Internship Opportunity")

    body_html = body.replace('\n', '<br>')
    html_body = f"""
    <html>
    <body>
        <p>{body_html}</p>
        <br>
        <img src="cid:signature" alt="Signature" style="width:500px;">
    </body>
    </html>
    """

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_body, 'html', 'utf-8'))

    if os.path.exists(signature_path):
        with open(signature_path, 'rb') as f:
            sig = MIMEImage(f.read())
            sig.add_header('Content-ID', '<signature>')
            sig.add_header('Content-Disposition', 'inline', filename='signature.png')
            msg.attach(sig)
    elif is_debug:
        print(f"⚠️ Signature file {signature_path} not found.")

    cv_path = cv_fr_path if language == 'fr' else cv_en_path
    if os.path.exists(cv_path):
        with open(cv_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename=\"{os.path.basename(cv_path)}\"')
            msg.attach(part)
    elif is_debug:
        print(f"⚠️ CV file {cv_path} not found.")

    return msg
