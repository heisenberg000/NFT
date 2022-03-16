#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/27 22:39
# @Author   : JAMES
# @File     : starark.py

import requests
import json, time, datetime,random
from urllib.parse import quote
import threading

class Starark(object):
    def __init__(self,cookie,uid):
        self.uid= uid
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36",
            "origin": "https://h5.stararknft.art",
            "referer": "https://h5.stararknft.art/",
            "token-no": "aa8c6985a8706a7f335354884135e92c",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": cookie
        }
        self.urls = {
            "create_list": {"url":"https://h5.stararknft.art/api/My/create_list","method":"post"},
            "box_detail": {"url":"https://h5.stararknft.art/api/Box/detailed","method":"post"},
            "box_buy_order": {"url":"https://h5.stararknft.art/api/Box/box1_other_byorder","method":"post"},
            "product_detail": {"url":"https://h5.stararknft.art/api/Product/detailed","method":"post"},
            "product_buy_order": {"url":"","method":"post"},
            "get_captcha": {"url":"https://h5.stararknft.art/api/VerifyCode/captcha?{ts}","method":"get"},
            "pay": {"url":"https://h5.stararknft.art/api/Pay/direct_buy_box","method":"post"}
        }


    def get_data(self,url_key,payload):
        data = {}
        while True:
            try:
                if self.urls[url_key]["method"] == "post":
                    resp = requests.post(url=self.urls[url_key]["url"], data=payload, headers=self.headers)
                if self.urls[url_key]["method"] == "get":
                    resp = requests.get(url=self.urls[url_key]["url"].format(**payload), headers=self.headers)
                if resp.status_code == 200:
                    print("(%s)请求返回(%s)：" % (url_key, resp.content))
                    if self.urls[url_key]["method"] == "get":
                        data = resp.content
                    if self.urls[url_key]["method"] == "post":
                        data = json.loads(resp.text)
                    break;
            except requests.exceptions.RequestException as e:
                pass
            except ConnectionError as e:
                pass
            except ConnectionResetError as e:
                pass
            except ConnectionAbortedError as e:
                pass
            except ConnectionRefusedError as e:
                pass
        return data

    def box_detail(self,id):
        payload = {
            "id": id,
            "uid": self.uid
        }
        detail = {}
        data = self.get_data(url_key="box_detail",payload=payload)
        if data.get("code",0) == 1 and data.get("msg","") == "success":
            detail["id"] = data["data"]["info"]["id"]
            detail["price"] = data["data"]["info"]["price"]
        return detail

    def get_captcha(self):
        payload = {"ts":int(round(time.time() * 1000))}
        bdata = self.get_data("get_captcha",payload=payload)
        with open(str(payload["ts"]) + ".PNG","wb") as f:
            f.write(bdata)

    def box_buy_order(self,id,page):
        payload = {
            "product_id": id,
            "pages": page,
            "gotosale": 1,
            "sort": 1,
            "uid": self.uid
        }
        valid_token_list = []
        data = self.get_data(url_key="box_buy_order",payload=payload)
        if data.get("code", 0) == 1 and data.get("msg", "") == "success":
            for row in data["data"]["rows"]:
                valid_token_list.append(row["token_id"])
        return valid_token_list

    def pay(self,token_id, price):
        payload = {
            "token_id": token_id,
            "password": 111111,
            "money": price,
            "uid": self.uid
        }
        while True:
            data = self.get_data(url_key="pay",payload=payload)
            if data.get("code",0) == 0 and data.get("msg","").find("UID已熔断") != -1:
                print("购买失败：%s" % (data.get("msg",""),))
                # time.sleep(3)
            if data.get("code",0) == 0 and data.get("msg","").find("手速慢了") != -1:
                print("购买失败：%s" % (data.get("msg",""),))
                break;
            if data.get("code",0) == 1:
                print("购买成功：%d" % (token_id,))
                # time.sleep(3)
                break;
        return token_id


def do(starark,valid_token_list,price,id):
    start_time = datetime.datetime.strptime('2022-03-16 15:00:00', '%Y-%m-%d %H:%M:%S')
    while True:
        if start_time < datetime.datetime.now():
            while len(valid_token_list) > 0:
                token_id = random.choice(valid_token_list)
                print("随机选择了可购买id：%d" % (token_id,))
                del_token_id = starark.pay(token_id=token_id, price=price)
                if token_id == del_token_id:
                    valid_token_list.remove(token_id)
            valid_token_list = starark.box_buy_order(id=id)
            print("新的可购买id列表：", valid_token_list)

# def mutilthread():
#     threads = []
#     t1 = threading.Thread(target=do,args=(starark,valid_token_list,price,id))
#     threads.append(t1)
#     t2 = threading.Thread(target=do, args=(starark, valid_token_list, price, id))
#     threads.append(t2)
#
#     for t in threads:
#         t.setDaemon(True)
#         t.start()
#
#     for t in threads:
#         t.join()

def main():
    # 初始化
    # boxtype = input("请输入类型：1.盲盒 2.非盲盒")
    # boxtype = int(boxtype)
    page = input("请输入要获取的可用token页数：")
    base_info = {
        "author_id": 10839,
        "id": 11116
    }
    starark = Starark(
        "PHPSESSID=7c5038dad05ba8986987ee26049a7dec; user={%22id%22:43202%2C%22mobile%22:%2215316693779%22%2C%22nickname%22:%22fxxkyou%22%2C%22img%22:%22/static/img/demo.png%22%2C%22backimg%22:%22/static/img/demo.png%22%2C%22content%22:%22%22%2C%22ETHaddress%22:%220xbd7363501587f2a223d38fb0f529d129f121941b%22%2C%22is_read_privacy_protocol%22:1}",
        43202)
    # 获取详情
    box_detail = starark.box_detail(id=base_info["id"])
    print("抢购基本信息：", box_detail)
    # 获取可用token，现获取500个
    valid_token_list = []
    for p in range(1,int(page)):
        valid_token_list.extend(starark.box_buy_order(id=base_info["id"],page=p))
    # 提前获取一次
    print("提前获取可购买编号：", valid_token_list)
    start_time = datetime.datetime.strptime('2022-03-16 15:00:00', '%Y-%m-%d %H:%M:%S')
    while True:
        if start_time < datetime.datetime.now():
            while len(valid_token_list) > 0:
                token_id = random.choice(valid_token_list)
                print("随机选择了可购买id：%d" % (token_id,))
                del_token_id = starark.pay(token_id=token_id, price=box_detail["price"])
                if token_id == del_token_id:
                    valid_token_list.remove(token_id)
            valid_token_list = starark.box_buy_order(id=base_info["id"])
            print("新的可购买id列表：", valid_token_list)

def atest():
    starark = Starark(
        "PHPSESSID=7c5038dad05ba8986987ee26049a7dec; user={%22id%22:43202%2C%22mobile%22:%2215316693779%22%2C%22nickname%22:%22fxxkyou%22%2C%22img%22:%22/static/img/demo.png%22%2C%22backimg%22:%22/static/img/demo.png%22%2C%22content%22:%22%22%2C%22ETHaddress%22:%220xbd7363501587f2a223d38fb0f529d129f121941b%22%2C%22is_read_privacy_protocol%22:1}",
        43202)
    starark.get_captcha()

if __name__ == '__main__':
    # main()
    atest()