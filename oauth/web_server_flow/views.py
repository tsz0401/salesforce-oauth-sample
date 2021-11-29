import requests
import oauth.common_const
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse


def get_html(request):
    redirect_uri = get_url_of_this_page(request)

    if "access_token" in request.COOKIES.keys():
        # When access_token is set, just show the page
        response = render(request, "web_server.html")
        return response
    elif "code" in request.GET:
        # When code is set, get access_token, and show the page
        code = request.GET.get("code")
        token_dict = get_token_from_sfdc(code, redirect_uri)
        response = render(request, "web_server.html")
        response.set_cookie('access_token', token_dict["access_token"])
        response.set_cookie('refresh_token', token_dict["refresh_token"])
        response.set_cookie('instance_url', token_dict["instance_url"])
        return response
    else:
        # When there is no code nor access_token, show login page
        login_url = get_sfdc_login_url(redirect_uri)
        response = redirect(login_url)
        return response


def get_url_of_this_page(request):
    redirect_uri = "{0}://{1}".format(request.scheme,
                                      request.get_host() + "/oauth/webserver/")
    return redirect_uri


def get_sfdc_login_url(redirect_uri):
    login_url = oauth.common_const.LOGIN_URL + "/services/oauth2/authorize"
    login_url += "?response_type=code"
    login_url += "&client_id=" + oauth.common_const.CLIENT_ID
    login_url += "&redirect_uri=" + redirect_uri
    return login_url


def get_token_from_sfdc(code, redirect_uri):
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
    return token_dict


def get_accounts(request):
    access_token = request.COOKIES.get("access_token")
    instance_url = request.COOKIES.get("instance_url")
    refresh_token = request.COOKIES.get("refresh_token")
    response = get_accounts_from_sfdc(
        instance_url, access_token, refresh_token)
    return response


def get_accounts_from_sfdc(instance_url, access_token, refresh_token):
    url = instance_url + "/services/data/v52.0/query?q=SELECT+name+from+Account"
    try:
        response = get_sfdc_records(url, access_token, refresh_token)
    except NeedReLoginError as e:
        response = create_response_to_force_re_login()
    return response


def get_sfdc_records(url, access_token, refresh_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    sfdc_response = requests.get(url, headers=headers)

    if sfdc_response.status_code < 300:
        # If it succeeded, return the data
        response = JsonResponse(sfdc_response.json())
        return response
    elif sfdc_response.status_code == 401:
        # If 401(Unauthorized) is returned, try to refresh token, and call the original request again
        token_dict = refresh_token_from_sfdc(refresh_token)
        if "access_token" in token_dict:
            access_token = token_dict["access_token"]
            headers = {
                'Authorization': 'Bearer ' + access_token
            }
            sfdc_response = requests.get(url, headers=headers)
            if sfdc_response.status_code < 300:
                response = JsonResponse(sfdc_response.json())
                response.set_cookie('access_token', token_dict["access_token"])
                response.set_cookie('instance_url', token_dict["instance_url"])
                return response

    if sfdc_response.status_code >= 300:
        raise NeedReLoginError("Re-Login is needed")


def refresh_token_from_sfdc(refresh_token):
    body = {
        "grant_type": "refresh_token",
        "client_id": oauth.common_const.CLIENT_ID,
        "client_secret": oauth.common_const.CLIENT_SECRET,
        "refresh_token": refresh_token
    }
    response = requests.post(
        oauth.common_const.LOGIN_URL + "/services/oauth2/token", body)
    token_dict = response.json()
    return token_dict


def create_response_to_force_re_login():
    response = JsonResponse({})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("instance_url")
    response.status_code = 401
    return response


class NeedReLoginError(Exception):
    pass
