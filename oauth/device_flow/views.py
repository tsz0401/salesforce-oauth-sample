import requests
import oauth.common_const
from django.shortcuts import render
from django.http import JsonResponse


def get_html(request):

    divice_request_result = send_device_request()

    rendering_param = {
        "user_code": divice_request_result["user_code"],
        "device_code": divice_request_result["device_code"],
        "verification_uri": divice_request_result["verification_uri"]
    }
    return render(request, "device.html", rendering_param)


def send_device_request():
    body = {
        "response_type": "device_code",
        "client_id": oauth.common_const.CLIENT_ID
    }
    response = requests.post(
        oauth.common_const.LOGIN_URL + "/services/oauth2/token", body)
    result = response.json()
    return result


def check_request_result(request):
    body = {
        "grant_type": "device",
        "client_id": oauth.common_const.CLIENT_ID,
        "code": request.GET.get("device_code")
    }
    response = requests.post(
        oauth.common_const.LOGIN_URL + "/services/oauth2/token", body)
    result = response.json()
    return JsonResponse(result)
