import requests
import json

url = "http://172.20.32.191:10001/server-sysmanager/queryAreaTree"  # 接口地址

# 消息头数据
headers = {
    'Connection': 'keep-alive',
    'Content-Length': '123',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://passport.csdn.net',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://passport.csdn.net/account/login?from=http://www.csdn.net',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '省略',

}

payload = {"id": "root",
           "flag": "1"}
date_json = json.dumps(payload)
# verify = False 忽略SSH 验证

r = requests.put(url, date_json,headers={"content-type": "application/json"})
print(r.json())