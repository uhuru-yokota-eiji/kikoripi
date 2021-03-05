from django.http.response import JsonResponse

from api.libs.bme280_handler import Bme280Handler
from api.libs.api_response import ApiResponse
from api.libs.grovepi_handler import GrovepiHandler
from api.libs.parse_api_params import ParseApiParams
from api.libs.tick import Tick


def write(request):
    """ HTTP/GET /write コール時の処理
    センサー名に応じて、デバイスに値を書き込む

    Args:
        request (QueryDict): リクエストパラメータ

    Returns:
        dict: クライアントに返すjson形式の値
    """

    params = request.GET.copy()
    api_response = ApiResponse()
    parse = ParseApiParams(params, mode="write")

    if parse.has_gp():
        try:
            # NOTICE: 初期化をすべてのpinに毎回実施するのが良いかは要調査　->　書き込み毎にやらないほうがいい。ポートの状態が一瞬でも変化することがありうる
            _init_gpio_output()
            # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
            value = int(parse.gp(0)["value"])
            GrovepiHandler.digitalWrite(parse.gp(0)["no"], value)
        except IndexError:
            api_response.failure("index Error")
        except Exception as e:
            api_response.failure(str(e))
        else:
            api_response.success()
            api_response.set_params({"value": value})

    # NOTICE: /writeでtickが"target"キーにある場合、"interval"もある前提
    if parse.has_tick():
        try:
            # NOTICE: 配列の最初固定。複数対応は必要なときに実施する
            Tick.update_interval(parse.tick(0)["interval"])
        except IndexError:
            api_response.failure("index Error")
        except Exception as e:
            api_response.failure(str(e))
        else:
            api_response.success()
            api_response.set_params({"interval": int(parse.tick(0)["interval"])})

    return JsonResponse(api_response.response)


def read(request):
    """HTTP/GET /read コール時の処理
    ADCのセンサー名に応じて、センサー値を読んで返す

    Args:
        request (QueryDict): リクエストパラメータ

    Returns:
        dict: クライアントに返すjson形式の値
    """
    params = request.GET.copy()
    api_response = ApiResponse()

    parse = ParseApiParams(params, mode="read")

    if parse.has_adc():
        try:
            adc_no = parse.adc(0)["no"]
            GrovepiHandler.pinMode(adc_no, "INPUT")
            sensor_value = GrovepiHandler.analogRead(adc_no)
        except IOError:
            # TODO: except句とエラーの種類を増やし、エラーメッセージをエラー内容にあわせる
            api_response.failure("No sensor found")
        except IndexError:
            api_response.failure("index Error")
        except Exception as e:
            api_response.failure(str(e))
        else:
            api_response.success()
            api_response.set_params({"value": sensor_value})

    return JsonResponse(api_response.response)


def sensor(request):
    """HTTP/GET /sensor コール時の処理
    ADC以外のセンサー値を読んで返す

    Args:
        request (QueryDict): リクエストパラメータ

    Returns:
        dict: クライアントに返すjson形式の値
    """
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
    """HTTP/GET /scan コール時の処理
    接続しているセンサー値一覧を返す

    Args:
        request (QueryDict): リクエストパラメータ

    Returns:
        dict: クライアントに返すjson形式の値
    """
    # NOTICE: 優先度が低いためdummyのI/Fだけ用意
    api_response = ApiResponse()
    api_response.success()
    api_response.value([{"name": "scaned_sensor_name", "id": "scaned_sensor_id"}])
    return JsonResponse(api_response.response)


def _init_gpio_output():
    """gpioのすべてのPINのモードをOUTPUTにする
    GPIOに書き込み時の初期化処理。
    """
    for no in range(8):
        GrovepiHandler.pinMode(no + 1, "OUTPUT")
