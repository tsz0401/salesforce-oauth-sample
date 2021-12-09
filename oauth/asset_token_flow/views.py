import requests
import json
import base64
import oauth.common_const
from django.shortcuts import render
from django.shortcuts import redirect


def get_html(request):
    redirect_uri = get_url_of_this_page(request)

    if "code" in request.GET:
        # When code is set, get access_token, and show the page
        code = request.GET.get("code")
        asset_token = get_token_from_sfdc(code, redirect_uri)
        rendering_param = {
            "asset_token": asset_token
        }
        response = render(request, "asset_token.html", rendering_param)
        return response
    else:
        # When there is no code nor access_token, show login page
        login_url = get_sfdc_login_url(redirect_uri)
        response = redirect(login_url)
        return response


def get_url_of_this_page(request):
    redirect_uri = "{0}://{1}".format(request.scheme,
                                      request.get_host() + "/oauth/asset_token/")
    return redirect_uri


def get_sfdc_login_url(redirect_uri):
    login_url = oauth.common_const.LOGIN_URL + "/services/oauth2/authorize"
    login_url += "?response_type=code"
    login_url += "&client_id=" + oauth.common_const.CLIENT_ID
    login_url += "&redirect_uri=" + redirect_uri
    return login_url


def get_token_from_sfdc(code, redirect_uri):
    # get access token
    body = {
        "grant_type": "authorization_code",
        "client_id": oauth.common_const.CLIENT_ID,
        "client_secret": oauth.common_const.CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "code": code
    }
    response = requests.post(
        oauth.common_const.LOGIN_URL + "/services/oauth2/token", body)
    token_dict = response.json()
    access_token = token_dict["access_token"]

    # get asset token
    body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
        "subject_token": access_token,
        "actor_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "actor_token": get_jwt()
    }
    response = requests.post(
        token_dict["instance_url"] + "/services/oauth2/token", body)
    asset_token_dict = response.json()

    return asset_token_dict["access_token"]


def get_jwt():
    header = {"alg": "none"}
    header_base64 = base64.b64encode(json.dumps(header).encode())

    payload = {
        "did": "test-device-001",
        "Name": "Asset Token For 001",
        "Asset": {
                "Name": "Asset 19730",
                "SerialNumber": "9461094121",
                "AccountId": "0015h00000MY3LyAAL"
        }
    }
    payload_base64 = base64.b64encode(json.dumps(payload).encode())
    result = header_base64.decode(
        "ascii") + "." + payload_base64.decode("ascii") + "."
    return result
