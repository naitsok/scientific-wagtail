from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.forms.auth import LoginForm

from captcha.fields import CaptchaField


class EmailLoginForm(LoginForm):
    """Adds captcha field to wagtail admin login form.
    Replace 'username' with 'email' to not to confuse the user."""
    username = forms.EmailField(
        max_length=255,
        widget=forms.TextInput(attrs={'tabindex': '1'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)

        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field('email')
        self.fields['username'].max_length = self.username_field.max_length or 254
        self.fields['username'].label = capfirst(self.username_field.verbose_name)

        self.fields['username'].widget.attrs['placeholder'] = (
            _("Enter your %s") % 'email'
        )
        self.fields['captcha'] = CaptchaField()
        self.fields['captcha'].widget.attrs['placeholder'] = 'Solve me'

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': 'email'},
        )