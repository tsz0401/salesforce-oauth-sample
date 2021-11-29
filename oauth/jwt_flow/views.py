import requests
import jwt
import oauth.common_const
import datetime
from django.shortcuts import render
from django.http import JsonResponse


def get_html(request):
    return render(request, "jwt.html")


def get_accounts(request):
    token_dict = get_token_from_sfdc()
    instance_url = token_dict["instance_url"]
    access_token = token_dict["access_token"]
    accounts = get_accounts_from_sfdc(instance_url, access_token)
    return JsonResponse(accounts)


def get_token_from_sfdc():
    body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": get_jwt()
    }
    response = requests.post(
        oauth.common_const.LOGIN_URL + "/services/oauth2/token", body)
    token_dict = response.json()
    return token_dict


def get_jwt():
    with open('oauth/jwt_flow/test.pem', mode='r') as f:
        secret = f.read()
        encoded = jwt.encode({
            'iss': oauth.common_const.CLIENT_ID,
            'aud': oauth.common_const.LOGIN_URL,
            'sub': oauth.common_const.USER_NAME,
            'exp': datetime.datetime.now().timestamp() + 60
        }, secret, algorithm='RS256')
    return encoded


def get_accounts_from_sfdc(instance_url, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(
        instance_url + "/services/data/v52.0/query?q=SELECT+name+from+Account", headers=headers)
    result = response.json()
    return result
