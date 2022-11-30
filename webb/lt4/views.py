from django.views.decorators.http import require_GET, require_POST
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from webpush import send_user_notification
import json


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        condition = ['head' not in data, 'body' not in data, 'id' not in data]
        if any(condition):
            return JsonResponse(status = 400, data = {"message" : "Invalid data format"})

        user_id = request.user

    except:
        pass