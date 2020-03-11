from django.http.response import JsonResponse
from grovepi import *


def write(request):
    init_gpio_output()

    response = request.GET

    target = response.get("target")
    value = response.get("value")
    gpio_no = parse_gpio_no(target)

    if is_gp_target(target) and value == "1":
        digitalWrite(gpio_no, 1)
    else:
        digitalWrite(gpio_no, 0)

    return JsonResponse(response)


def read(request):
    response = request.GET
    return JsonResponse(response)


def parse_gpio_no(target_str):
    return int(target_str.replace("GP", ""))


def is_gp_target(target_str):
    return target_str.startswith("GP")


def init_gpio_output():
    for no in range(8):
        pinMode(no + 1, "OUTPUT")
