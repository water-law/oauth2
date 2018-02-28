[Description]

The project reference Ruan Yifeng teacher Sina Weibo SDK code Provide simple github

Oauth2.0 authentication sdk, I hope later to integrate all well-known sites

Oauth2.0 sdk, the project is in its infancy, will continue to add, no Feel free to

welcome requests.

[说明]

本项目参考了阮一峰老师新浪微博SDK的代码

提供简单的 github Oauth2.0 认证 sdk,

以后希望能集成所有知名常用网站的 Oauth2.0

sdk，项目处于开始阶段， 以后会不断补充，不

足之处， 欢迎 pull requests。

[使用]
```
import requests
from .github import APIClient

def callback(request):
    app_key = "you app_key"
    app_secret = "you app_secret"
    redirect_uri = "you redirect_uri"
    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=redirect_uri)

    # 处理回调接口时， Github 服务器返回一个 code
    code = request.GET.get("code")
    d= client.request_access_token(code=code)
    # https://api.github.com/user 是获取用户信息的接口
    user_info = requests.get("https://api.github.com/user",params={"access_token": d["access_token"]})


urlpatterns = [
    url(r'^github/oauth/callback$', callback), # 'github/oauth/callback' replace with you callback address.
]
```