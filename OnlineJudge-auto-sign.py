# /usr/bin/env python3
# -*- coding: utf-8 -*-
# 导入库
import configparser
import json
import logging
import os

import requests

# log模块
logging.basicConfig(filename="log.log", level=logging.INFO, format='[%(asctime)s][%(levelname)s]: %(message)s', encoding="utf-8")
printlog = logging.StreamHandler()
printlog.setFormatter(logging.Formatter(fmt="\033[0;33m[%(asctime)s]%(level)s\033[0m: %(message)s", datefmt="%X"))
printlogger = logging.getLogger()
printlogger.addHandler(printlog)


def log(level, message):
    if level == "info":
        logging.info(message, extra={"level": '\033[1;34m[信息]'})
    if level == "error":
        logging.error(message, extra={"level": '\033[1;31m[错误]'})


# 配置文件
os.chdir(os.path.dirname(os.path.abspath(__file__)))
config = configparser.RawConfigParser()
config.read("config.ini", encoding="utf-8")

# API
# url地址
url = config["config"]["url"]
# 登录地址
login = url + "/api/login"
# 用户信息地址
userinfo = url + "/api/profile"
# 签到地址
sighin = url + "/api/sighin"
# 方糖微信推送地址
ftqq = "https://sc.ftqq.com/" + config["config"]["ftqq"] + ".send?text="


# 登录
def post_login(username, password):
    #for _ in range(1, 10):
    #    password = base64.b64decode(password).decode("utf-8")
    log("info", "正在登录中......")
    headers["Cookie"] = "csrftoken=gnW1iou7O0fvueeGyENEEfDV4mPdob6BnISwCxMx3Li6pXpsmner56kwGn18denc"
    headers["X-CSRFToken"] = "gnW1iou7O0fvueeGyENEEfDV4mPdob6BnISwCxMx3Li6pXpsmner56kwGn18denc"
    try:
        response = requests.post(url=login, json={"username": username, "password": password}, headers=headers)
        post = json.loads(response.text)
    except:
        log("error", "登录失败,请检查配置文件")
        return "error"
    else:
        if post["data"] == "Succeeded":
            log("info", "登录成功")
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            account[i]["cookies"] = "csrftoken=" + cookies["csrftoken"] + ";sessionid=" + cookies["sessionid"]
            headers["Cookie"] = account[i]["cookies"]
            headers["X-CSRFToken"] = account[i]["cookies"][10:74]
            with open("account.json", "w", encoding="utf-8") as f:
                json.dump(account, f, ensure_ascii=False, indent=4)
            log("info", "保存 cookie 成功")
            return account[i]["cookies"]
        else:
            log("error", "登录失败, 请检查用户名或密码")
            log("error", "错误信息:")
            log("error", post)
            return "error"


# 计算等级
def level(experience):
    if experience >= 0 and experience <= 99:
        return "小白兔"
    if experience >= 100 and experience <= 199:
        return "菜鸟"
    if experience >= 200 and experience <= 499:
        return "键盘虾"
    if experience >= 500 and experience <= 999:
        return "马农"
    if experience >= 1000 and experience <= 4999:
        return "牛人"
    if experience >= 5000 and experience <= 9999:
        return "程序猿"
    if experience > 9999:
        return "攻城狮"


# 签到
def signin(cookies):
    try:
        post = json.loads(requests.post(url=sighin, headers=headers).text)
        if post["data"] == "Singined":
            log("info", "稳健佬, 您已经签过到了呀~明天再来哦")
        elif post["data"]["info"] == "Success":
            log("info", "签到成功")
            log("info", "获得稳点: " + str(post["data"]["experience"]))
        else:
            log("error", "签到失败")
            log("error", "错误信息:")
            log("error", post)
            return "error"
    except:
        log("error", "签到失败")
        return "error"
    sign_info = json.loads(requests.get(url=sighin, headers=headers).text)
    info = json.loads(requests.get(url=userinfo, headers=headers).text)
    if sign_info["error"] == None:
        log("info", "连续签到天数: " + str(sign_info["data"]["continue_sighin_days"]))
        log("info", "上次签到时间: " + str(sign_info["data"]["last_sighin_time"]))
        log("info", "当前稳点: " + str(info["data"]["experience"]))
        log("info", "当前等级: " + level(int(json.dumps(info["data"]["experience"]))))
    else:
        log("error", "查询签到状态失败")
        log("error", "错误信息:")
        log("error", sign_info)
        return "error"


if __name__ == '__main__':
    log("info", "自动签到任务启动")
    with open("account.json", encoding="utf-8") as f:
        account = json.load(f)
    for i in range(0, len(account)):
        if account[i]["username"] == "" or account[i]["password"] == "":
            log("error", "用户名或密码为空,跳过执行")
            continue
        log("info", "=========账号 " + account[i]["username"] + " 开始执行===================================")
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Cookie": account[i]["cookies"],
            "X-CSRFToken": account[i]["cookies"][10:74],
            "Connection": "close"
        }
        if signin(account[i]["cookies"]) == "error":
            log("info", "尝试重新登录中......")
            if post_login(account[i]["username"], account[i]["password"]) == "error":
                log("error", "重新登录失败!")
            else:
                signin(account[i]["cookies"])
        log("info", "=========账号 " + account[i]["username"] + " 执行完毕===================================")
    log("info", "任务完成\n")
    if config["config"]["ftqqapi"] != "":
        requests.post(url=ftqq + "任务完成")
