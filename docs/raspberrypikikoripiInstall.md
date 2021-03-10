# kikoripiのインストール

- リポから落とす

kikoripiを「home/pi/」に設置することをおすすめします。
```
cd ~
git clone https://github.com/uhuru-yokota-eiji/kikoripi.git
cd kikoripi
```

- 必要なパッケージのインストール

```
pip install -r requirements/staging.txt
cp .env.staging .env
```

- DjangoのDBテーブルの初期化

```
python manage.py make migrations
python manage.py migrate
```

- migrationsせずにDBテーブルの初期化（必須ではない）
```
python manage.py migrate --run-syncdb
```

- kikoripiの起動確認
```
python manage.py runserver localhost:3000
```