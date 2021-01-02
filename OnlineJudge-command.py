# /usr/bin/env python3
# -*- coding: utf-8 -*-
# 导入库
import configparser
import getpass
import json
import logging
import os
import re

import colorama
import prettytable
import requests
import time

colorama.init()
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
# 获取问题地址
gt_problem = url + "/api/problem"
tj_problem = url + "/api/submission"
# 获取公告地址
announcement = url + "/api/announcement?offset=0&limit=10"
# 方糖推送地址
ftqq = "https://sc.ftqq.com/" + config["config"]["ftqq"] + ".send?text="
# 请求头文件
headers = {
    "Content-Type": "application/json;charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Cookie": "",
    "X-CSRFToken": "",
    "Connection": "close"
}


# 主菜单
def menu():
    global info
    if config["config"]["auto_signin"] == "True":
        auto_sign()
        return
    headers["Cookie"] = config["config"]["cookies"]
    headers["X-CSRFToken"] = config["config"]["cookies"][10:74]
    try:
        info = json.loads(requests.get(url=userinfo, headers=headers).text)
        username = info["data"]["user"]["username"]
    except:
        log("error", "使用 cookies 登录失败，请重新登录")
        log("info", "请输入账号和密码")
        username = input("账号: ")
        password = getpass.getpass("密码: ")
        post_login(username, password)
        try:
            info = json.loads(requests.get(url=userinfo, headers=headers).text)
            username = info["data"]["user"]["username"]
        except:
            return
    while True:
        print("\033[0;30m                \033[1;34m[菜单]\033[0m")
        log("info", "欢迎来到主菜单, 帮助中心: ")
        log("info", "cookie     重新获取 cookie")
        log("info", "info       获取基本信息")
        log("info", "problem    题目列表")
        log("info", "signin     签到")
        log("info", "exit       退出")
        print("\033[1;36m[" + info["data"]["user"]["username"] + "]\033[0m", end="")
        into = input("> ")
        if into == "cookie":
            log("info", "请输入账号和密码")
            username = input("账号: ")
            password = getpass.getpass("密码: ")
            post_login(username, password)
            info = json.loads(requests.get(url=userinfo, headers=headers).text)
        elif into == "info":
            get_info()
        elif into == "signin":
            signin()
        elif into == "problem":
            problem_list(1, "")
        elif into == "exit":
            log("info", "正在退出!")
            return
        else:
            log("error", "输入无效, 请重新输入")


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
            cookies = "csrftoken=" + cookies["csrftoken"] + ";sessionid=" + cookies["sessionid"]
            headers["Cookie"] = cookies
            headers["X-CSRFToken"] = cookies[10:74]
            if config["config"]["auto_signin"] == "True":
                account[i]["cookies"] = "csrftoken=" + cookies["csrftoken"] + ";sessionid=" + cookies["sessionid"]
                with open("account.json", "w", encoding="utf-8") as f:
                    json.dump(account, f, ensure_ascii=False, indent=4)
            else:
                config.set("config", "cookies", cookies)
                with open("config.ini", "w", encoding="utf-8") as cookies:
                    config.write(cookies)
            log("info", "保存 cookie 成功")
        else:
            log("error", "登录失败, 请检查用户名或密码")
            log("error", "错误信息:")
            log("error", post)
            return "error"


def get_info():
    log("info", "正在获取用户信息......")
    if info["data"]:
        log("info", "数据id: " + str(info["data"]["id"]))
        log("info", "用户id: " + str(info["data"]["user"]["id"]))
        log("info", "用户名: " + str(info["data"]["user"]["username"]))
        log("info", "邮箱: " + str(info["data"]["user"]["email"]))
        log("info", "用户组: " + str(info["data"]["user"]["admin_type"]))
        log("info", "问题权限: " + str(info["data"]["user"]["problem_permission"]))
        log("info", "注册时间: " + info["data"]["user"]["create_time"][:10] + " " + info["data"]["user"]["create_time"][11:19])
        log("info", "最后登录时间: " + info["data"]["user"]["last_login"][:10] + " " + info["data"]["user"]["last_login"][11:19])
        log("info", "两步验证: " + str(info["data"]["user"]["two_factor_auth"]))
        log("info", "api是否被禁用: " + str(info["data"]["user"]["open_api"]))
        log("info", "账号是否被禁用: " + str(info["data"]["user"]["is_disabled"]))
        log("info", "真实姓名: " + str(info["data"]["real_name"]))
        #log("info", "ACM问题状态: " + str(info["data"]["acm_problems_status"]))
        #log("info", "OI问题状态: " + str(info["data"]["oi_problems_status"]))
        log("info", "头像地址: " + url + str(info["data"]["avatar"]))
        log("info", "博客: " + str(info["data"]["blog"]))
        log("info", "心情: " + str(info["data"]["mood"]))
        log("info", "Github地址: " + str(info["data"]["github"]))
        log("info", "学校: " + str(info["data"]["school"]))
        log("info", "专修: " + str(info["data"]["major"]))
        log("info", "语言: " + str(info["data"]["language"]))
        log("info", "年级: " + str(info["data"]["grade"]))
        log("info", "AC题数: " + str(info["data"]["accepted_number"]))
        log("info", "总成绩: " + str(info["data"]["total_score"]))
        log("info", "提交编号: " + str(info["data"]["submission_number"]))
        log("info", "当前稳点: " + str(info["data"]["experience"]))
        log("info", "当前等级: " + level(int(json.dumps(info["data"]["experience"]))))
    else:
        log("error", "获取失败! ")


def problem_list(page, keywords):
    print("\033[0;30m                \033[1;34m[题目列表]\033[0m")
    offset = (page - 1) * 20
    problemlist = json.loads(requests.get(url=gt_problem + "?limit=20&offset=" + str(offset) + "&keywords=" + keywords, headers=headers).text)
    problem_detail = prettytable.PrettyTable(["状态", "题号", "题目", "难度", "提交总数", "通过率"])
    total = problemlist["data"]["total"]
    for n in range(min(20, total)):
        my_status = problemlist["data"]["results"][n]["my_status"]
        _id = problemlist["data"]["results"][n]["_id"]
        title = problemlist["data"]["results"][n]["title"]
        difficulty = problemlist["data"]["results"][n]["difficulty"]
        submission_number = problemlist["data"]["results"][n]["submission_number"]
        accepted_number = problemlist["data"]["results"][n]["accepted_number"]
        if submission_number == 0:
            acv = "0%"
        else:
            acv = str(int(accepted_number) / int(submission_number) * 100)[:5] + "%"
        problem_detail.add_row([color(my_status), _id, title, color(difficulty), submission_number, acv])
    log("info", "\n" + str(problem_detail))
    log("info", "                              第 " + str(page) + " 页 共 " + str(total // 20 + 1) + " 页")
    while True:
        log("info", "欢迎来到题目列表, 帮助中心: ")
        log("info", "goto 题号    查看题号题目")
        log("info", "search 题目  搜索题目")
        log("info", "page 页码    跳转指定页码")
        log("info", "return       返回")
        print("\033[1;36m[" + info["data"]["user"]["username"] + "]\033[0m", end="")
        into = input("> ")
        if into == "return":
            return
        elif into[:4] == "page" and len(into) > 5 and into[6:].isdigit():
            problem_list(int(into[5:]))
        elif into[:4] == "goto" and len(into) > 5:
            problem_info(into[5:], "")
        elif into[:6] == "search" and len(into) > 8:
            problem_list(1, into[7:])
        #problem_id = titlelist.get(into, "None")
        #if problem_id != "None":
        else:
            log("error", "输入错误, 请重新输入")


def problem_info(_id):
    global probleminfo
    print("\033[0;30m                \033[1;34m[题目详细]\033[0m")
    cls = re.compile(r'<[^>]+>', re.S)
    probleminfo = json.loads(requests.get(url=gt_problem + "?problem_id=" + _id, headers=headers).text)
    log("info", cls.sub('', "题目: " + probleminfo["data"]["title"]))
    log("info", cls.sub('', "描述: " + probleminfo["data"]["description"]))
    log("info", cls.sub('', "输入: " + probleminfo["data"]["input_description"]))
    log("info", cls.sub('', "输出: " + probleminfo["data"]["output_description"]))
    samples_id = 0
    while True:
        try:
            log("info", "输入样例" + str(samples_id + 1) + ":" + str(probleminfo["data"]["samples"][samples_id]["input"]))
            log("info", "输出样例" + str(samples_id + 1) + ":" + str(probleminfo["data"]["samples"][samples_id]["output"]))
            samples_id += 1
        except:
            break
    log("info", cls.sub('', "提示: " + str(probleminfo["data"]["hint"])))
    log("info", "来源: \033[0m" + str(probleminfo["data"]["source"]))
    log("info", "统计: \033[0m")
    for x in range(-2, 8):
        try:
            log("info", color(x) + ": " + str(probleminfo["data"]["statistic_info"][str(x)]))
        except:
            continue
    while True:
        print("\n\033[0;30m                \033[1;34m[题目详细]\033[0m")
        log("info", "post     提交")
        log("info", "return   返回")
        print("\033[1;36m[" + info["data"]["user"]["username"] + "]\033[0m", end="")
        into = input("> ")
        if into == "post":
            post_problem(probleminfo["data"]["id"])
        elif into == "return":
            return
        else:
            log("error", "输入错误, 请重新输入")


def post_problem(pid):
    languages = probleminfo["data"]["languages"]
    try:
        with open("code.txt", mode="r", encoding="utf-8") as code:
            codes = code.read()
    except:
        log("error", "未找到 code.txt, 正在创建......")
        with open("code.txt", mode="w", encoding="utf-8"):
            log("info", "创建成功!")
        return
    b = input("已找到 code.txt 文件, 是(Y)否(N)使用?默认Y: ")
    if b != "Y" and b != "" and b != "y":
        log("info", "取消")
        return
    log("info", "提交语言可选: ")
    for x in languages:
        print('"' + x + '", ', end="")
    into = input("\n请输入提交语言, 默认 C++: ")
    if into in languages:
        language = into
        log("info", "已选择: " + language)
    else:
        language = "C++"
        log("info", "已选择: " + language)
    log("info", "正在提交中.....")
    post = json.loads(requests.post(url=tj_problem, json={"problem_id": pid, "language": language, "code": codes}, headers=headers).text)
    submission(post["data"]["submission_id"])


def submission(submission_id):
    submissioninfo = json.loads(requests.get(url=tj_problem + "?id=" + submission_id, headers=headers).text)
    if submissioninfo["data"]["result"] == 6 or submissioninfo["data"]["result"] == 7:
        log("info", "查询状态中......")
        time.sleep(3)
        submission(submission_id)
    else:
        print("\033[0;30m                \033[1;34m[提交结果]\033[0m")
        log("info", "提交状态: " + color(submissioninfo["data"]["result"]))
        if submissioninfo["data"]["result"] != -2 and submissioninfo["data"]["result"] != 5:
            log(
                "info", "时间: " + str(submissioninfo["data"]["statistic_info"]["time_cost"]) + "ms   内存: " +
                str(submissioninfo["data"]["statistic_info"]["memory_cost"] // 1048576) + "MB   语言: " + submissioninfo["data"]["language"] +
                "   提交者: " + str(submissioninfo["data"]["username"]))
            log("info", "各个评测点状态: ")
            submission_list = prettytable.PrettyTable(["测试点", "状态", "内存", "CPU用时", "真实用时", "分数", "返回值"])
            id = 0
            while True:
                try:
                    result = color(submissioninfo["data"]["info"]["data"][id]["result"])
                    memory = str(submissioninfo["data"]["info"]["data"][id]["memory"] // 1048576) + "MB"
                    cpu_time = str(submissioninfo["data"]["info"]["data"][id]["cpu_time"]) + "ms"
                    real_time = str(submissioninfo["data"]["info"]["data"][id]["real_time"]) + "ms"
                    signal = submissioninfo["data"]["info"]["data"][id]["signal"]
                    exit_code = submissioninfo["data"]["info"]["data"][id]["exit_code"]
                    id += 1
                    submission_list.add_row([id, result, memory, cpu_time, real_time, signal, exit_code])
                except:
                    break
            log("info", "\n" + str(submission_list))
        else:
            log("error", "错误信息: " + submissioninfo["data"]["statistic_info"]["err_info"])
        log("info", "提交id: " + str(submissioninfo["data"]["id"]))
        log("info", "提交时间: " + str(submissioninfo["data"]["create_time"][:10] + " " + submissioninfo["data"]["create_time"][11:19]))
        log("info", "提交ip: " + str(submissioninfo["data"]["ip"]))
        log("info", "代码: \n" + str(submissioninfo["data"]["code"]))
        log("info", "分享状态: " + str(submissioninfo["data"]["shared"]))

        while True:
            print("\033[0;30m                \033[1;34m[提交结果]\033[0m")
            log("info", "share    切换分享状态")
            log("info", "return   返回")
            print("\033[1;36m[" + info["data"]["user"]["username"] + "]\033[0m", end="")
            into = input("> ")
            if into == "share":
                requests.put(url=tj_problem,
                             data=json.dumps({
                                 "id": submission_id,
                                 "shared": bool(1 - submissioninfo["data"]["shared"])
                             }),
                             headers=headers)
                submissioninfo = json.loads(requests.get(url=tj_problem + "?id=" + submission_id, headers=headers).text)
                log("info", "当前分享状态: " + str(submissioninfo["data"]["shared"]))
            elif into == "return":
                return
            else:
                log("error", "输入错误, 请重新输入")


# 签到


def signin():
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
    sign_info = json.loads(requests.get(url=sighin, headers=headers).text)
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


# 计算等级


def level(experience):
    if experience >= 0 and experience <= 99:
        return "\033[1;46m小白兔\033[0m"
    if experience >= 100 and experience <= 199:
        return "\033[1;44m菜鸟\033[0m"
    if experience >= 200 and experience <= 499:
        return "\033[1;45m键盘虾\033[0m"
    if experience >= 500 and experience <= 999:
        return "\033[1;42m马农\033[0m"
    if experience >= 1000 and experience <= 4999:
        return "\033[1;43m牛人\033[0m"
    if experience >= 5000 and experience <= 9999:
        return "\033[1;41m程序猿\033[0m"
    if experience > 9999:
        return "\033[1;40m攻城狮\033[0m"


def color(color):
    #####提交状态#####
    if color == -2 or color == "CE":
        return "\033[1;35m编译错误\033[0m"
    elif color == -1 or color == "WA":
        return "\033[1;31m答案错误\033[0m"
    elif color == 0 or color == "AC":
        return "\033[1;32m通过\033[0m"
    elif color == 1 or color == 2 or color == "TLE":
        return "\033[1;31m超过时间限制\033[0m"
    elif color == 3 or color == "MLE":
        return "\033[1;31m超过空间限制\033[0m"
    elif color == 4 or color == "RE":
        return "\033[1;31m运行错误\033[0m"
    elif color == 5 or color == "SE":
        return "\033[1;31m系统错误\033[0m"
    elif color == 6 or color == "Pending":
        return "\033[1;36m待定中\033[0m"
    elif color == 7 or color == "Judging":
        return "\033[0;36m评测中\033[0m"
    elif color == 8 or color == "PAC":
        return "\033[1;36m部分正确\033[0m"
    #####难度#####
    elif color == "High":
        return "\033[1;41m 高 \033[0m"
    elif color == "Mid":
        return "\033[1;44m 中 \033[0m"
    elif color == "Low":
        return "\033[1;42m 低 \033[0m"
    else:
        return "-"


def auto_sign():
    log("info", "自动签到任务启动")
    with open("account.json", encoding="utf-8") as f:
        account = json.load(f)
    for i in range(0, len(account)):
        if account[i]["username"] == "" or account[i]["password"] == "":
            log("error", "用户名或密码为空,跳过执行")
            continue
        log("info", "=========账号 " + account[i]["username"] + " 开始执行===================================")
        headers["Cookie"] = account[i]["cookies"]
        headers["X-CSRFToken"] = account[i]["cookies"][10:74]
        if signin(account[i]["cookies"]) == "error":
            log("info", "尝试重新登录中......")
            if post_login(account[i]["username"], account[i]["password"]) == "error":
                log("error", "重新登录失败!")
            else:
                signin(account[i]["cookies"])
        log("info", "=========账号 " + account[i]["username"] + " 执行完毕===================================")
    log("info", "任务完成\n")


if __name__ == '__main__':
    # 主菜单
    try:
        menu()
    except KeyboardInterrupt:
        print("\n")
        log("info", "正在退出!")
    if config["config"]["ftqq"] != "":
        requests.post(url=ftqq + "任务完成")
