from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.dispatch import receiver

from devsearch.devsearch.settings import EMAIL_HOST_USER

from .models import Profile
from django.conf import settings

# ADD SETTING IN APPS FOR SIGNALS

# @receiver(post_save, sender=Profile)


def createProfile(sender, instance, created, **kwargs):
    if created:  # check if it is the first instance
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )
        subject = 'Welcome',
        message = 'Welcome to devsearch',

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=True
        )

# when profile is deleted the user should also be deleted


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
# post_delete.connect(deleteUser, sender=Profile)


@receiver(post_save, sender=Profile)
def updateUser(instance, created, sender, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
