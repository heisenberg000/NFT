#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/27 22:39
# @Author   : JAMES
# @File     : starark.py

import requests
import json, time, datetime,random
from urllib.parse import quote

class Starark(object):
    def __init__(self,cookie,uid=42274):
        self.uid= uid
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
            "origin": "https://h5.stararknft.art",
            "referer": "https://h5.stararknft.art/",
            "token-no": "aa8c6985a8706a7f335354884135e92c",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": cookie
        }


    def get_data(self,url,payload):
        code = 0
        resp_dict = {}
        while code != 200:
            try:
                response = requests.get(url=url,data=payload,headers=self.headers)
                if response.status_code == 200:
                    resp_dict = json.loads(response.text)
                    code = 200
            except requests.exceptions.RequestException as e:
                pass
            except ConnectionError as e:
                pass
            except ConnectionResetError as e:
                pass
            except ConnectionRefusedError as e:
                pass
        return resp_dict

    def get_phpsessid(self):
        url = "https://h5.stararknft.art/undefined"
        resp = requests.get(url, headers=self.headers)
        print(resp.headers["set-cookie"])
        if resp.headers["set-cookie"] != "":
            sessid = resp.headers["set-cookie"].split(";")[0]
            return sessid
            # self.cookies.set(sessid[0],sessid[1])
            # ck_str = ";".join(['%s=%s' % (name, value) for (name, value) in self.cookies.items()])
            # print("ck_str", ck_str)
            # self.headers["cookie"] = ck_str
        return None


    def login(self):
        url = "https://h5.stararknft.art/api/Login/login_password"
        payload = {
            "mobile": "16621121712",
            "password": "heisenberg001"
        }
        user = {}
        data = self.get_data(url=url,payload=payload)
        if data["code"] == 1 and data["msg"] == "success":
            user["id"] = data["data"]["id"]
            user["mobile"] = data["data"]["mobile"]
            user["ETHaddress"] = data["data"]["ETHaddress"]
        return user


    def create_list(self,author_id,page):
        url = "https://h5.stararknft.art/api/My/create_list"
        payload = {
            "author_id": author_id,
            "gotosale": "",
            "name": "",
            "issue_type": "",
            "pages": page,
            "uid": self.uid
        }
        nft_list = []
        data = self.get_data(url,payload)
        if data["code"] == 1 and data["msg"] == "success":
            for row in data["data"]["rows"]:
                nft_list.append({"id":row["id"],"price":row["price"]})
        return nft_list

    def index(self):
        url = "https://h5.stararknft.art/api/Product/index"
        payload = {
            "pages": 1,
            "name": "",
            "issue_type":"",
            "sellout": "",
            "typeid": 0,
            "sort":"",
            "uid": 43202
        }

    def detail(self,id):
        url = "https://h5.stararknft.art/api/Box/detailed"
        payload = {
            "id": id,
            "uid": self.uid
        }
        can_buy = False
        data = self.get_data(url=url,payload=payload)
        if data["code"] == 1 and data["msg"] == "success":
            if data["data"]["status"] == 2 or data["data"]["status"] == 1:
                can_buy = True
        return can_buy

    def buy_productorder(self,id):
        url = "https://h5.stararknft.art/api/Product/other_byorder"
        payload = {
            "product_id": id,
            "pages": 1,
            "gotosale": 1,
            "uid": self.uid
        }
        product_list = []
        data = self.get_data(url=url, payload=payload)
        if data.get("code", 0) == 1 and data.get("msg", "") == "success":
            for row in data["data"]["rows"]:
                product_list.append(row["token_id"])
        return product_list

    def buy_boxorder(self,id,page):
        url = "https://h5.stararknft.art/api/Box/box1_other_byorder"
        payload = {
            "product_id": id,
            "pages": page,
            "gotosale": 1,
            "sort": 1,
            "uid": self.uid
        }
        box_list = []
        data = self.get_data(url=url,payload=payload)
        if data.get("code", 0) == 1 and data.get("msg", "") == "success":
            for row in data["data"]["rows"]:
                box_list.append(row["token_id"])
        return box_list



    def pay(self,token_id, price):
        url = "https://h5.stararknft.art/api/Pay/direct_buy_box"
        payload = {
            "token_id": token_id,
            "password": 111111,
            "money": price,
            "uid": self.uid
        }
        pay_flag = False
        while not pay_flag:
            data = self.get_data(url=url,payload=payload)
            if data.get("code", 0) == 0 and data.get("msg", "").find("UID已熔断") != -1:
                time.sleep(1)
            if (data.get("code",0) == 0 and data.get("msg","").find("手速慢了") != -1) or (data.get("code", 0) == 1):
                pay_flag = True
        return pay_flag


def main():
    # 初始化
    # product : 1,box : 0
    type = 1
    starark = Starark("user={%22id%22:43202%2C%22mobile%22:%2215316693779%22%2C%22nickname%22:%22fxxkyou%22%2C%22img%22:%22/static/img/demo.png%22%2C%22backimg%22:%22/static/img/demo.png%22%2C%22content%22:%22%22%2C%22ETHaddress%22:%220xbd7363501587f2a223d38fb0f529d129f121941b%22}; PHPSESSID=ab85a45ae54f1d3c957d4061387e1f5d",43202)
    # 先登录获取uid
    # user = starark.login()
    # print("user:", user)
    # # 获取PHPSESSID
    # starark.set_cookie()
    # print(starark.headers)
    # print(starark.cookies)
    # 获取nft信息
    # 获取作者第一页列表
    nft_list = starark.create_list(author_id=5174)
    # 获取所有可购买物品
    if len(nft_list) > 0:
        for nft in nft_list:
            if starark.detail(id=nft["id"]):
                nft["token_list"] = []
                # 提前获取所有可购买nft的可购买token_id，取1-50页数据
                for i in range(1,51,1):
                    if type == 0:
                        info = starark.buy_boxorder(id=id,page=i)
                    else:
                        info = starark.buy_productorder(id=id,page=i)
                    nft["token_list"].extend(info)
            else:
                nft_list.remove(nft)
    print("可购买的nft—id列表:", nft_list)

    start_time = datetime.datetime.strptime('2022-03-10 18:00:00', '%Y-%m-%d %H:%M:%S')
    while True:
        if start_time < datetime.datetime.now():
            # 获取当前随机到的nft值
            # by_info = starark.byorder(id=ntf_info["id"])
            while True:
                if len(nft_list) > 1:
                    nft = random.choice(nft_list)
                else:
                    nft = nft_list[0]
                tid = random.choice(nft["token_list"])
                if starark.pay(token_id=tid,price=nft["price"]):
                    if tid in nft["token_list"]:
                        print("删除货号id=%d下的无效token_id=%d",(nft["id"],tid))
                        nft["token_list"].remove(tid)
                    else:
                        if type == 0:
                            token_list = starark.buy_boxorder(id=nft["id"])
                        else:
                            token_list = starark.buy_productorder(id=nft["id"])
                        print("获取新的可购买编号token列表", token_list)
                        nft["token_list"] = token_list

if __name__ == '__main__':
    main()
