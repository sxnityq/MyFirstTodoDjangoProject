from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.core.mail import EmailMessage

from django.conf import settings


def get_user_default_profile_image():
    return "default/default_user_profile.jpg"


def get_profile_image_filepath(self, filename):
    return f"profile_images/{self.pk}/{filename}"


def custom_send_mail(request, user):

    current_site = get_current_site(request)

    context = {
        'token': default_token_generator.make_token(user),
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'domain': current_site
    }

    message = render_to_string(template_name='main/registration/verify_email.html',
                               context=context,
                               request=request)

    the_mail = EmailMessage(
        subject='VERIFY MESSAGE',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email, ]
    )
    the_mail.send()
