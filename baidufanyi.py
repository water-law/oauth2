# -*- coding: utf-8 -*-
# 本接口仅支持 python3
import json
import collections
from http import client as httplib
from urllib import request as urllib
import hashlib
import random

appid = ''  # 你的appid
secretKey = ''  # 你的密钥


class APIError(Exception):
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        Exception.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (
            self.error_code, self.error, self.request)


class XRequest:

    def __init__(self, api_domain):
        self.api_domain = api_domain
        self.httpClient = httplib.HTTPConnection(self.api_domain)

    def _encode_params(self, **kw):
        """
        do url-encode parameters
        >>> _encode_params(a=1, b='R&D')
        'a=1&b=R%26D'
        >>> _encode_params(a=u'\u4e2d\u6587', b=['A', 'B', 123])
        'a=%E4%B8%AD%E6%96%87&b=A&b=B&b=123'
        """
        args = []
        for k, v in kw.items():
            if isinstance(v, str):
                qv = v
                args.append('%s=%s' % (k, urllib.quote(qv)))
            elif isinstance(v, collections.Iterable):
                for i in v:
                    qv = i if isinstance(i, str) else str(i)
                    args.append('%s=%s' % (k, urllib.quote(qv)))
            else:
                qv = str(v)
                args.append('%s=%s' % (k, urllib.quote(qv)))

        return '&'.join(args)

    def request(self, method, url, params):
        target = None
        url = '%s?%s' % (url, self._encode_params(**params))
        self.httpClient.request(method, url)
        response = self.httpClient.getresponse()
        result = json.loads(response.read().decode())
        if 'error_code' in result.keys():
            error_code = int(result['error_code'])
            error = str(result['error_msg'])
            if error_code in [52001, 52002, 54003, 54005]:
                self.httpClient.close()
                return target
            else:
                raise APIError(error_code=error_code, error=error, request='{scheme}://{domain}{url}'.format(
                    scheme='http',
                    domain="api.fanyi.baidu.com",
                    url=url
                ))
        else:
            target = result['trans_result'][0]['dst']
        self.httpClient.close()
        return target


class BaiduTranslator:

    def __init__(self, appid, secretKey):
        self.appid = appid
        self.secretKey = secretKey
        self.api_domain = "api.fanyi.baidu.com"
        self.url = '/api/trans/vip/translate'
        self._request = XRequest(self.api_domain)

    def generate_sign(self, text):
        salt = random.randint(32768, 65536)
        sign = self.appid + text + str(salt) + self.secretKey
        m = hashlib.md5()
        m.update(sign.encode())
        m.digest()
        return {"salt": str(salt), "sign": m.hexdigest()}

    def translate(self, sl, tl, text):
        params = {
            "appid": self.appid,
            "from": sl,
            "to": tl,
            "q": text
        }
        signs = self.generate_sign(text)
        params.update(signs)
        return self._request.request(
            "GET",
            self.url,
            params
        )


if __name__ == '__main__':
    trans = BaiduTranslator(appid, secretKey)
    rs = trans.translate("en", "zh", "apple")
    print(rs)
