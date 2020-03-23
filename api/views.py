from django.http.response import JsonResponse
from grovepi import *
from api.libs import bme280
from api.models import TickInterval


def write(request):
    # NOTICE: 初期化をすべて毎回実施するのが良いかは要調査
    init_gpio_output()

    response = request.GET.copy()

    target = response.get("target")
    value = response.get("value")
    interval = response.get("interval")
    gpio_no = parse_gpio_no(target)

    if is_gp_target(target) and value == "1":
        digitalWrite(gpio_no, 1)
    else:
        digitalWrite(gpio_no, 0)

    if(t := TickInterval.objects.all().first()):
        t.interval = int(interval)
        t.save()
    else:
        TickInterval.objects.create(interval=interval)
    return JsonResponse(response)


def read(request):
    response = request.GET.copy()

    target = response.get("target")
    adc_no = parse_adc_no(target)

    pinMode(adc_no, "INPUT")
    try:
        sensor_value = analogRead(adc_no)
    except IOError:
        print("Error")
    else:
        response["value"] = sensor_value

    return JsonResponse(response)


def sensor(request):
    params = request.GET.copy()
    # ids = params.getlist("ids")

    data = bme280.main()
    # print(data)
    response = {
        # ids[0]: data
        "BME0": data # とりいそぎ固定
    }
    return JsonResponse(response)


def scan(request):
    return JsonResponse({"result": True})


def parse_gpio_no(target_str):
    return int(target_str.replace("GP", ""))


def parse_adc_no(target_str):
    '''
    A(n) Port is Pin (n+14) Port
    ex) A0 Port is Pin 14 Port
    '''
    return int(target_str.replace("ADC", "")) + 14


def is_gp_target(target_str):
    return target_str.startswith("GP")


def init_gpio_output():
    for no in range(8):
        pinMode(no + 1, "OUTPUT")
