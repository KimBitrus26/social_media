from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

EMAIL_VERIFICATION_LINK = settings.EMAIL_VERIFICATION_LINK

class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, email_confirmation):
        return f'{EMAIL_VERIFICATION_LINK}?key={email_confirmation.key}'
