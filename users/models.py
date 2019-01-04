# custom user model to login with email
# From django docs: "creating custom user model is
# highly recommended when starting new project.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    
    # Make email field unique to use it for authentication.
    # Otherwise keep usual username as primary username, but
    # use email to log in.
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    class Meta:
        # create indexes for user lookup by username and email.
        indexes = [
            models.Index(fields=['username',]),
            models.Index(fields=['email',]),
        ]