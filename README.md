# kikoriPi+

## About

raspi上で動く、WSS(Web Sensor Server)とgrovePi+のセンサー（GPIO, ADC, DAC, I2C）ドライバー群

## Environment

### software
* python 3.8.1
* Django 3.0.4

### hardware
* RaspberryPi 3 Model b+
* GrovePi+
  * ADC Sensor. Ex: [Light Sensor](http://wiki.seeedstudio.com/Grove-Light_Sensor/)
  * DAC Sensor. Ex: [LED Socket Kit](http://wiki.seeedstudio.com/Grove-LED_Socket_Kit/)
  * I2C Sensor. Ex: [BME280](http://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/)


## Install & Run

```
git clone https://github.com/uhuru-yokota-eiji/kikoripi
cd kikoripi/

# 開発環境の場合
pip install/develop.txt
cp .env.develop .env

# RaspberryPi 上の場合
#pip install/staging.txt
#cp .env.staging .env

python mannage.py runserver localhost:3000
```

## 動作確認

HTTP/GET
```
% curl http://localhost:3000/scan
{"result": "success", "msg": "Success", "v": [{"name": "scaned_sensor_name", "id": "scaned_sensor_id"}]}
```
websocket
```
% wscat -c ws://localhost:3000/ws
Connected (press CTRL+C to quit)
> {"op":"scan"}
< {"result": "success", "msg": "Success", "v": [{"name": "scaned_sensor_name", "id": "scaned_sensor_id"}]}
```
