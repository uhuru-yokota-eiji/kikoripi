from django.http.response import JsonResponse

from api.libs import bme280
from api.libs.parse_api_params import ParseApiParams
from api.libs.tick import Tick

from grovepi import *


def write(request):
    params = request.GET.copy()
    # NOTICE: 初期化をすべて毎回実施するのが良いかは要調査
    _init_gpio_output()

    parse = ParseApiParams(params, mode="write")
    response = {"result": "success", "msg": "Success"}
    response["target"] = parse.target

    if parse.has_gp():
        # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
        value = int(parse.gp(0)["value"])
        digitalWrite(parse.gp(0)["no"], value)
        response["value"] = value

    # NOTICE: /writeでtickがtargetにある場合、intervalもある前提
    if parse.has_tick():
        # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
        Tick.update_interval(parse.tick(0)["interval"])
        response["interval"] = int(parse.tick(0)["interval"])

    # TODO: 失敗時のメッセージ処理

    return JsonResponse(response)


def read(request):
    params = request.GET.copy()
    parse = ParseApiParams(params, mode="read")

    response = params

    adc_no = parse.adc(0)["no"]

    try:
        pinMode(adc_no, "INPUT")
        sensor_value = analogRead(adc_no)
    except IOError as e:
        response["result"] = "error"
        response["msg"] = "No sensor found"
    else:
        response["result"] = "success"
        response["value"] = sensor_value

    return JsonResponse(response)


def sensor(request):
    params = request.GET.copy()
    response = {}

    params["ids"] = params.getlist("ids")
    parse = ParseApiParams(params, mode="sensor")
    if parse.has_bme():
        response["BME0"] = bme280.main()
        # response[parse.bme(0)["name"]] = {"hoge": "fuga"}
    if parse.has_tick():
        # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
        tick = Tick(parse.tick(0)["no"])
        response[parse.tick(0)["name"]] = tick.sensor_value

    return JsonResponse(response)


def scan(request):
    # NOTICE: 優先度が低いためI/Fだけ用意
    return JsonResponse({"result": True})


def _init_gpio_output():
    for no in range(8):
        pinMode(no + 1, "OUTPUT")
