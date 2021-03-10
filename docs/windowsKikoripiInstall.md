# kikoripiのインストール

- リポから落とす
```
git clone https://github.com/uhuru-yokota-eiji/kikoripi.git
cd kikoripi
```

- 必要なパッケージのインストール
```
pip install -r requirements/develop.txt
copy .env.develop .env
```

- DjangoのDBテーブルの初期化
```
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