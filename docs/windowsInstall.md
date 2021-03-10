# 開発環境（Windows）へのインストール手順

## Python3.8.1環境のインストール

- Python to 3.8.1のインストール

[Python 3.8.1のリリースページ](https://www.python.org/downloads/release/python-381/)から
[Windows x86-64 executable installer](https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe)をダウンロードし、インストールする

- pipコマンドのアップグレード
```
python -m pip install --upgrade pip
```

- Python　3.8.1のWindows版では、Twisted未対応なので、以下の修正が必要
```
C:\＜python インストールフォルダー＞\Lib\site-packages\twisted\internet\asyncioreactor.py
```

修正部分
```
...
from twisted.python.log import callWithLogger
from twisted.internet.interfaces import IReactorFDSet

#try:
#    from asyncio import get_event_loop
#except ImportError:
#    raise ImportError("Requires asyncio.")

#replaced
import sys

try:
    from asyncio import get_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy
except ImportError:
    raise ImportError("Requires asyncio.")

if sys.platform == 'win32':
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
#replaced

# As per ImportError above, this module is never imported on python 2, but
# pyflakes still runs on python 2, so let's tell it where the errors come from.
from builtins import PermissionError, BrokenPipeError
...
```

- コマンドラインでwebsocketのテスト用（必須ではない）
Node-jsが必要になります。
```
npm install -g wscat
```