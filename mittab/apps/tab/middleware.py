import re

from django.contrib.auth.views import LoginView

from mittab.apps.tab.helpers import redirect_and_flash_info

LOGIN_WHITELIST = ("/accounts/login/", "/pairings/pairinglist/",
                   "/pairings/missing_ballots/", "/e_ballots/", "/404/",
                   "/403/", "/500/", "/teams/", "/judges/", "/json")

EBALLOT_REGEX = re.compile(r"/e_ballots/\S+")


class Login:
    """This middleware requires a login for every view"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        whitelisted = (request.path in LOGIN_WHITELIST) or \
                EBALLOT_REGEX.match(request.path)

        if not whitelisted and request.user.is_anonymous:
            if request.POST:
                view = LoginView.as_view(template_name="registration/login.html")
                return view(request)
            else:
                return redirect_and_flash_info(
                    request,
                    "You must be logged in to view that page",
                    path="/accounts/login/?next=%s" % request.path)
        else:
            return self.get_response(request)
