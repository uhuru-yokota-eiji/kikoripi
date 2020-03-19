"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # TODO: url_〇〇は毎回ファイル追加になるので、もっとスマートな/write /readの用意をしたい
    path('write', include('api.urls_write')),
    path('read', include('api.urls_read')),
    path('sensor', include('api.urls_sensor')),
    path('scan', include('api.urls_scan')),
    path('admin/', admin.site.urls),
]
