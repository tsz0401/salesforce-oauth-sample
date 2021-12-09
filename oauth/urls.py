import oauth.device_flow.views
import oauth.user_agent_flow.views
import oauth.hybrid_flow.views
import oauth.pkce_flow.views
import oauth.asset_token_flow.views
import oauth.web_server_flow.views
import oauth.jwt_flow.views
import oauth.password_flow.views
import oauth.views
from django.urls import path, include

from django.contrib import admin

admin.autodiscover()


# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("oauth/", oauth.views.get_html),

    path("oauth/password/", oauth.password_flow.views.get_html),
    path("oauth/password/accounts", oauth.password_flow.views.get_accounts),

    path("oauth/jwt/", oauth.jwt_flow.views.get_html),
    path("oauth/jwt/accounts", oauth.jwt_flow.views.get_accounts),

    path("oauth/webserver/", oauth.web_server_flow.views.get_html),
    path("oauth/webserver/accounts", oauth.web_server_flow.views.get_accounts),

    path("oauth/useragent/", oauth.user_agent_flow.views.get_html),
   
    path("oauth/hybrid/", oauth.hybrid_flow.views.get_html),

    path("oauth/pkce/", oauth.pkce_flow.views.get_html),

    path("oauth/asset_token/", oauth.asset_token_flow.views.get_html),

    path("oauth/device/", oauth.device_flow.views.get_html),
    path("oauth/device/check_request_result", oauth.device_flow.views.check_request_result),
]
