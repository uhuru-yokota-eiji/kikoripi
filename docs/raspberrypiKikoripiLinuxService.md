# ラズパイの起動時にkikoripiを立ち上げる方法

kikoripiを起動時に実行する方法の一つは、Linuxサービスとして実行することです。

## kikoripiサービスのインストール

設定上kikoripiを「home/pi/kikoripi」フォルダーに置く必要があります。

 - kikoripiサービスをシステムにコピーする

```
cd ~/kikoripi
sudo cp kikoripi.service /etc/systemd/system/kikoripi.service
```

 - kikoripiサービスを開始する
```
sudo systemctl start kikoripi.service
```

 - システム起動時にkikoripiサービスを有効する
```
sudo systemctl enable kikoripi.service
```

## その他のkikoripiサービス関連コマンド

 - サービスの実行状態の確認

```
systemctl status kikoripi
● kikoripi.service - kikoripi device service
   Loaded: loaded (/etc/systemd/system/kikoripi.service; disabled; vendor preset: enabled)
   Active: active (running) since Fri 2021-02-26 13:56:26 JST; 594ms ago
. . .
 2月 26 13:56:26 raspberrypi systemd[1]: Started kikoripi device service.
```

 - kikoripiサービス実行時にログがsyslogに出力されます。ログの確認方法
```
tail /var/log/syslog
```

 - kikoripiサービスを停止する
```
sudo systemctl stop kikoripi.service
```

 - kikoripiサービスファイルを変更後実行
```
systemctl daemon-reload
```