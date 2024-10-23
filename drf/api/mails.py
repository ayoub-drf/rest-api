from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_confirmation(user, modified):
    subject = f'Your {modified.__class__.__name__} has been updated!'
    html_message = render_to_string('email/confirmation_email.html', {'user': user, 'modified': modified})
    plain_message = strip_tags(html_message)
    from_email = 'noreply@example.com'
    
    send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)