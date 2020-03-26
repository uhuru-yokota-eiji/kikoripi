from django.http.response import JsonResponse

from api.libs.bme280_handler import Bme280Handler
from api.libs.api_response import ApiResponse
from api.libs.grovepi_handler import GrovepiHandler
from api.libs.parse_api_params import ParseApiParams
from api.libs.tick import Tick


def write(request):
    params = request.GET.copy()
    parse = ParseApiParams(params, mode="write")
    api_response = ApiResponse()

    # NOTICE: 初期化をすべて毎回実施するのが良いかは要調査
    _init_gpio_output()

    if parse.has_gp():
        # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
        value = int(parse.gp(0)["value"])
        GrovepiHandler.digitalWrite(parse.gp(0)["no"], value)
        api_response.set_params({"value": value})

    # NOTICE: /writeでtickがtargetにある場合、intervalもある前提
    if parse.has_tick():
        # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
        Tick.update_interval(parse.tick(0)["interval"])
        api_response.set_params({"interval": int(parse.tick(0)["interval"])})

    # TODO: 失敗時の処理
    api_response.success()

    return JsonResponse(api_response.response)


def read(request):
    params = request.GET.copy()
    parse = ParseApiParams(params, mode="read")
    api_response = ApiResponse(params)

    adc_no = parse.adc(0)["no"]

    try:
        GrovepiHandler.pinMode(adc_no, "INPUT")
        sensor_value = GrovepiHandler.analogRead(adc_no)
    except IOError as e:
        # TODO: exceptの例外の種類とエラーメッセージをあわせる
        api_response.failure("No sensor found")
    else:
        api_response.success()
        api_response.set_params({"value": sensor_value})

    return JsonResponse(api_response.response)


def sensor(request):
    params = request.GET.copy()
    api_response = ApiResponse()

    params["ids"] = params.getlist("ids")
    parse = ParseApiParams(params, mode="sensor")
    if parse.has_bme():
        api_response.set_params({"BME0": Bme280Handler.main()})
    if parse.has_tick():
        # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
        tick = Tick(parse.tick(0)["no"])
        api_response.set_params({parse.tick(0)["name"]: tick.sensor_value})

    return JsonResponse(api_response.response)


def scan(request):
    # NOTICE: 優先度が低いためI/Fだけ用意
    return JsonResponse({"result": True})


def _init_gpio_output():
    for no in range(8):
        GrovepiHandler.pinMode(no + 1, "OUTPUT")
