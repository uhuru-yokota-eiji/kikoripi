# 対応コマンド内容について

以下のコマンドは開発寛容においての実行結果となっております。
RasbberryPiでのテストは未実施です。

## 正常系

```
curl "http://localhost:3000/sensor?ids=BME0"
{"BME0": {"timestamp": 1614917797.0227861, "temperature": 12.3, "pressure": 1234.567, "humidity": 45.67}}
```

```
curl "http://localhost:3000/write?target=GP0&value=1"
{"result": "success", "msg": "Success", "value": 1}
```

```
curl "http://localhost:3000/read?target=ADC0"
{"result": "success", "msg": "Success", "value": 999.999}
```

```
curl "http://localhost:3000/write?target=TICK0&interval=100"
{"result": "success", "msg": "Success", "interval": 100}
```

## 異常系

```
curl "http://localhost:3000/write?target=GP&value=5"
{"result": "error", "msg": "index Error"}
```

```
curl "http://localhost:3000/read?target=ADC"
{"result": "error", "msg": "index Error"}
```

```
curl "http://localhost:3000/write?target=TICK&interval=100"
{"result": "error", "msg": "index Error"}
```

Noのチェック未実施
```
curl "http://localhost:3000/sensor?ids=BME"
{"BME0": {"timestamp": 1614919323.9628928, "temperature": 12.3, "pressure": 1234.567, "humidity": 45.67}}
```