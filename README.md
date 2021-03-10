# kikoriPi+

## About

raspi上で動く、WSS(Web Sensor Server)とgrovePi+のセンサー（GPIO, ADC, I2C）ドライバー群

## Environment

### software
* python 3.8.1
* Django 3.0.4

### hardware
* RaspberryPi 3 Model b+
* GrovePi+
  * GPIO Sensor. Ex: [LED Socket Kit](http://wiki.seeedstudio.com/Grove-LED_Socket_Kit/)
  * ADC Sensor. Ex: [Light Sensor](http://wiki.seeedstudio.com/Grove-Light_Sensor/)
  * I2C Sensor. Ex: [BME280](http://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/)


## 開発環境（Windows）インストール手順

* [環境インストール手順](docs/windowsInstall.md)
* [kikoripiのインストール手順](docs/windowsKikoripiInstall.md)

## RaspberryPi環境用インストール手順
* [環境インストール手順](docs/raspberrypiInstall.md)
* [kikoripiのインストール手順](docs/raspberrypikikoripiInstall.md)
* [起動時にkikoripiを立ち上げる方法](docs/raspberrypiKikoripiLinuxService.md)

## 動作確認

HTTP/GET
```
% curl "http://localhost:3000/scan"
{"result": "success", "msg": "Success", "v": [{"name": "scaned_sensor_name", "id": "scaned_sensor_id"}]}
```
WebSocket
```
% wscat -c ws://localhost:3000/ws
Connected (press CTRL+C to quit)
> {"op":"scan"}
< {"result": "success", "msg": "Success", "v": [{"name": "scaned_sensor_name", "id": "scaned_sensor_id"}]}
```

## Feature

Interfaceは [kikori](https://gitlab.com/myst3m/kikori/) を参考に作成しています。

* [HTTP/GET](https://gitlab.com/myst3m/kikori#httpget)
* [WebSocket](https://gitlab.com/myst3m/kikori#websocket)

* [対応コマンド内容について](docs/commandAPI.md)

### 仮想デバイス(TICK)

TICKは、WebSocketのIntervalと連動していて、Intervalで設定した周期でOn/Offを繰り返します

ex)
```
% wscat -c ws://localhost:8000/ws
Connected (press CTRL+C to quit)
> {"op": "listen", "v":["TICK0"]}
< {"result": "success", "msg": "Success"}
< {"TICK0": 1}
< {"TICK0": 0}
< {"TICK0": 1}
< {"TICK0": 0}
・・・
```
