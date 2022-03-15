#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/14 19:05
# @Author   : JAMES
# @File     : ztag


import requests
import execjs
import json

class ZTAG(object):
    def __init__(self,uuid):
        self.headers = {
            "app-channel": "11",
            "app-uuid": uuid,
            "Authorization": "Bearer",
            "Host": "app.ztag.vip",
            "Origin": "https://m.ztag.vip",
            "Referer": "https://m.ztag.vip/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
            "Content-Type": "application/json"
        }
        self.session = requests.session()

    def get_data(self,url,payload = {},method = "GET"):
        ret_data = {}
        while True:
            try:
                if method.upper() == "POST":
                    response = self.session.post(url = url,json = payload,headers=self.headers,timeout=5)
                else:
                    response = self.session.get(url = url,headers=self.headers,timeout=5)
                if response.status_code == 200:
                    ret_data = json.loads(response.text)
                    print("返回头：", response.headers)
                    print("返回数据：", ret_data)
                    break
            except requests.exceptions.RequestException as e:
                pass
            except ConnectionError as e:
                pass
            except ConnectionResetError as e:
                pass
            except ConnectionRefusedError as e:
                pass
        return ret_data

    # 登录获取并设置token
    def login(self,user):
        url = "https://app.ztag.vip/v1/apis/login"
        data = self.get_data(url = url,payload = user, method= "POST")
        if data["code"] == 200 and data["msg"] == "ok":
            self.headers["Authorization"] = "Bearer " + data["data"]["access_token"]

    def get_goods_info(self,good_id):
        url = "https://app.ztag.vip/v1/apis/goods_info?id={id}".format(id=good_id)
        good_info = {}
        data = self.get_data(url = url)
        if data["code"] == 200 and data["msg"] == "ok":
            good_info["id"] = good_id
            good_info["user_id"] = data["data"]["user_id"]
            good_info["limit_num"] = data["data"]["limit_num"]
        print("本次抢购项目：",good_info)
        return good_info

    # 获取首页NFT可购买项目列表
    def get_home_list(self):
        url = "https://app.ztag.vip/v1/apis/home_list?page=1&page_size=10&homepage_category=0"
        onsale = []
        data = self.get_data(url=url)
        if data["code"] == 200 and data["msg"] == "ok":
            for item in data["data"]["result"]:
                if item["sold"] != item["stock"]:
                    onsale.append({"id": item["id"],"name": item["name"], "price": item["price"]})
        print("在售列表：",onsale)
        return onsale

    def get_goods_orders(self,order):
        url = "https://order.ztag.vip/v1/apis/goods_orders"
        # order = {
        #     "id": id,
        #     "amount": amount
        # }
        data = self.get_data(url = url, payload = order)
        if data["code"] == 200 and data["msg"] == "ok":
            print(data["data"])



def getUUid():
    with open("./ztag.js", "r", encoding="utf-8") as f:
        ctx = execjs.compile(f.read())
    result = ctx.call("uuid")
    print("获得的uuid：%s" % (result,))
    return result

def main():
    # get_goods_info()
    # get_goods_orders(238,1)
    # getUUid()
    uuid = getUUid()
    zt = ZTAG(uuid)
    zt.login({"phone":"16621121712","password":"Hsg1990"})
    onsale = zt.get_home_list()
    if len(onsale) > 0:
        zt.get_goods_info(onsale[0]["id"])


if __name__ == '__main__':
    main()
