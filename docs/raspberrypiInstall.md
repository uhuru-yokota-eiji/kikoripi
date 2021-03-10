# RaspberryPiへのインストール

## Python3.8.1環境のインストール

- ラズパイを最新版にする
```
sudo apt update
sudo apt upgrade
```

- Pythonに必要なパッケージのインストール
```
sudo apt install -y git openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev
```

- Pythonのバージョンを簡単に変えられるツール「pyenv」のインストール
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

- pyenvを 「~/.bash_profile」に追加
```
sudo nano ~/.bash_profile
```

- 追加内容
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

- 「.bash_profile」の読み込み
```
source ~/.bash_profile
```

- 「pyenv」の実行確認（バージョン表示）
```
pyenv --version
->pyenv 1.2.23-9-g2c02f4f0
```

- インストール可能なPythonバージョンの確認（必須ではない）
```
pyenv install --list
```

- Python 3.8.1のインストール
```
pyenv install 3.8.1
```

- 現在のPythonバージョンの確認
```
python3 --version
->Python 3.7.3
```

- Pythonバージョンを3.8.1に変更
```
pyenv global 3.8.1
```

- Pythonバージョンが3.8.1であることを確認
```
python3 --version
->Python 3.8.1
```

- pipコマンドのアップグレード
```
pip install --upgrade pip
```

- コマンドラインでwebsocketのテスト用（必須ではない）
```
npm install -g wscat
```
