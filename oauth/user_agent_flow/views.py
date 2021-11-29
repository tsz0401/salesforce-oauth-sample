import oauth.common_const
from django.shortcuts import render


def get_html(request):
    rendering_param = {
        "login_url": oauth.common_const.LOGIN_URL,
        "client_id": oauth.common_const.CLIENT_ID
    }
    return render(request, "user_agent.html", rendering_param)
