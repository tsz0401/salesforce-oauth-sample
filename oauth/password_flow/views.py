import json
import requests
import oauth.common_const
from django.shortcuts import render
from django.http import JsonResponse


def get_html(request):
    return render(request, "password.html")


def get_accounts(request):
    token_dict = get_token_from_sfdc()
    instance_url = token_dict["instance_url"]
    access_token = token_dict["access_token"]
    accounts = get_accounts_from_sfdc(instance_url, access_token)
    return JsonResponse(accounts)


def get_token_from_sfdc():
    body = {
        "grant_type": "password",
        "client_id": oauth.common_const.CLIENT_ID,
        "client_secret": oauth.common_const.CLIENT_SECRET,
        "username": oauth.common_const.USER_NAME,
        "password": oauth.common_const.PASSWORD
    }
    response = requests.post(
        oauth.common_const.LOGIN_URL + "/services/oauth2/token", body)
    token_dict = response.json()
    return token_dict


def get_accounts_from_sfdc(instance_url, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(
        instance_url + "/services/data/v52.0/query?q=SELECT+name+from+Account", headers=headers)
    result = response.json()
    return result
