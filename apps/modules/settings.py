from cgitb import html, text
from pydoc import plain
from django import template
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.tokens import default_token_generator


# MultiThreading
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class SendMail():
    def Send_OPT(email, pin):
        subject = f"Augustine University Exeat Platform Email Verification:  {pin}"
        plaintext = template.loader.get_template("account/management/email/email.txt")
        htmltemp = template.loader.get_template("account/management/email/email_verification.html")
        c = {
            "email": email,
            "domain":"",
            "site_name":"Augustine University Exeat Platform",
            "otp": pin,
        }
        text_content = plaintext.render(c)
        html_content = htmltemp.render(c)
        email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=settings.EMAIL_HOST_USER, to=[email], headers = {'Reply-To': settings.EMAIL_HOST_USER})
        email.attach_alternative(html_content, "text/html")
        # email.send()
        # Start Email Threading
        EmailThread(email).start()