import requests
import base64
import os
import json
import traceback

class OCR:
    def __init__(self):
        pass

    def ocr(self, url):
        headers = {
            'authority': 'aidemo.youdao.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://ai.youdao.com',
            'referer': 'https://ai.youdao.com/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        f = requests.get(url).content
        b64 = base64.b64encode(f)
        data = {
            'imgBase': 'data:image/jpeg;base64,' + str(b64, encoding='utf8'),
            'lang': '',
            'company': '',
        }

        response = requests.post('https://aidemo.youdao.com/ocrtransapi1', headers=headers, data=data,
                                 proxies={'http': None, 'https': None})

        if response.status_code == 200:
            try:
                js = response.json()
                if "renderImage" in list(js.keys()):
                    img = js["renderImage"]
                    return base64.b64decode(img)
                else:
                    return json.dumps(js, ensure_ascii=False)
            except Exception as e:
                traceback.print_exc()
                return str(e)
        else:
            return f"{response.status_code} - {response.text}"
