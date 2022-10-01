from time import sleep
from django.db.models.signals import *
from django.dispatch import receiver
from django.core.mail import *
from django.core.signals import *
from .models import *
from .views import *
from django.template.loader import *


@receiver(post_save, sender=Response)
def send_response_email(created, instance, *args, **kwargs):
    if created:
        post_author = instance.response_to.user
        subject = f'{post_author}'
        response_user = instance.response_user
        post_author_email = instance.response_to.user.email

        send_mail(
            subject=subject,
            message=f"Greetings, {post_author}\n"
                    f"There's a new response to your post\n"
                    f"from - {response_user}\n",
            from_email='',
            recipient_list=[post_author_email])
