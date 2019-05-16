# _*_coding:utf-8_*_
import json
from django.http import HttpResponse


def json_return(json_data, ensure_ascii=True):
    return HttpResponse(json.dumps(json_data, ensure_ascii=ensure_ascii), content_type="application/json")


def get_client_ip(request):
    ip = ""
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip
