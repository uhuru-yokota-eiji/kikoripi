from django.http.response import JsonResponse
from grovepi import *


def index(request):
    # print("index")

    led = 2
    pinMode(led, "OUTPUT")

    response = request.GET

    # print(type(response))
    # print(response)

    if response.get("target") == "GPIO2" and response.get("value") == "1":
        digitalWrite(led, 1)
    else:
        digitalWrite(led, 0)

    return JsonResponse(response)
