#!usr/bin/python3
# -*- coding: utf-8 -*-
#导入库
import requests, json, sys, logging, os, getpass, prettytable, colorama, configparser
colorama.init()

def color(color):
    #####log日志#####
    if color == "info": color = '\033[1;34m[信息]'
    elif color == "error": color = '\033[1;31m[错误]'
    #####提交状态#####
    elif color == -2 or color == "CE": color = "\033[1;35m编译错误\033[0m"
    elif color == -1 or color == "WA": color = "\033[1;31m答案错误\033[0m"
    elif color == 0 or color == "AC": color = "\033[1;32m通过\033[0m"
    elif color == 1 or color == 2 or color == "TLE": color = "\033[1;31m超过时间限制\033[0m"
    elif color == 3 or color == "MLE": color = "\033[1;31m超过空间限制\033[0m"
    elif color == 4 or color == "RE": color = "\033[1;31m运行错误\033[0m"
    elif color == 5 or color == "SE": color = "\033[1;31m系统错误\033[0m"
    elif color == 6 or color == "Pending": color = "\033[1;36m待定中\033[0m"
    elif color == 7 or color == "Judging": color = "\033[0;36m评测中\033[0m"
    elif color == 8 or color == "PAC": color = "\033[1;36m部分正确\033[0m"
    #####难度#####
    elif color == "High": color = "\033[1;41m 高 \033[0m"
    elif color == "Mid": color = "\033[1;44m 中 \033[0m"
    elif color == "Low": color = "\033[1;42m 低 \033[0m"
    else: color = "-"
    return color

#log模块
logger = logging.getLogger()
filelog = logging.FileHandler("log.log", encoding="utf-8")
filelog.setFormatter(logging.Formatter(fmt="[%(asctime)s][%(levelx)s][%(title)s][%(message)s]"))
printlog = logging.StreamHandler()
printlog.setFormatter(logging.Formatter(fmt="\033[0;33m[%(asctime)s]%(color)s\033[0m[%(message)s]", datefmt="%X"))
logger.addHandler(filelog)
logger.addHandler(printlog)

def log(level, title, message):
    logger.error(message, extra={'title': title,'levelx':level, 'color': color(level)})

headers = {"Content-Type": "application/json;charset=utf-8",
    "Cookie": "csrftoken=dvTfFYvCObIY7toKDE3NQI2PicjSo7Pisub1wuRhwLHBHODSbjJjWRw103eVeK6T",
    "X-CSRFToken": "dvTfFYvCObIY7toKDE3NQI2PicjSo7Pisub1wuRhwLHBHODSbjJjWRw103eVeK6T",
    "Connection": "close"
    }

cmddir = os.getcwd()+"\\config.ini"
config = configparser.RawConfigParser()
config.read(cmddir, encoding="utf-8")

if config.has_option("config", "url") and config.has_option("config", "auto_signin") and config.has_option("config", "cookies"): error = 0
else:
    log("error", "配置", "config.ini 文件出错, 正在重新创建......")
    config.add_section("config")
    config["config"] = {"url": "", "auto_signin": "0", "cookies": ""}
    with open(cmddir, "w", encoding="utf-8") as configfile : config.write(configfile)
    log("info", "配置", "创建成功! 文件位于: " + cmddir)

if config["config"]["url"] != "" and config["config"]["auto_signin"] != "":
    url = config["config"]["url"]
    cookie = config["config"]["cookies"]
    auto_signin = config["config"]["auto_signin"]
else:
    log("error", '配置', "请先配置 config.ini!! 文件位于: " + cmddir)
    os.system("pause")
    sys.exit()

cookie = config["config"]["cookies"]
#错误
error = 0
#登录地址
login = url + "/api/login"
#用户信息地址
userinfo = url + "/api/profile"
#签到地址
sighin = url + "/api/sighin"
#获取问题地址
gt_problem = url + "/api/problem?"
tj_problem = url + "/api/submission?id="
#获取公告地址
#announcement = url + "/api/announcement?offset=0&limit=10"

#主菜单
def menu():
    global error, get2, auto_signin
    title = "主菜单"
    log("info", title, "有错误一般都是 cookie 错误, 尝试重新获取 cookies 一般都可解决")
    #检查 cookie文件是否存在
    check_cookies()
    if auto_signin == "1":
        log("info", title, "自动签到模式已开启")
        post_sign()
        get_sign()
        sys.exit()
    else:
        log("info", title, "自动签到模式已关闭")
    log("info", title, "欢迎来到主菜单, 帮助中心: ")
    log("info", title, "cookie     重新获取 cookie")
    log("info", title, "info       获取基本信息")
    log("info", title, "problem    题目列表")
    log("info", title, "signin     签到")
    log("info", title, "exit       退出")
    log("info", title, "cls        清屏")
    while True :
        print("\033[0;30m++++++++++++++++++++++++++++++++++\033[1;34m[菜单]\033[0m")
        if error == 1 :
            into = input("游客>")
        else:
            print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m", end="")
            into = input(">")
        if into == "help":
            log("info", title, "帮助中心 : ")
            log("info", title, "cookie     重新获取 cookie")
            log("info", title, "info       获取基本信息")
            log("info", title, "problem    题目列表")
            log("info", title, "signin     签到")
            log("info", title, "exit       退出")
            log("info", title, "cls        清屏")
        elif into == "cookie":
            get_cookies()
            check_cookies()
        elif into == "info":
            os.system("cls")
            get_info()
        elif into == "signin":
            os.system("cls")
            post_sign()
            get_sign()
        elif into == "problem":
            os.system("cls")
            problem_list()
        elif into == "cls": os.system("cls")
        elif into == "exit":
            log("error", title, "正在退出!!")
            sys.exit()
        else: log("error", title, "输入无效, 请重新输入")

#登录
def post_login():
    global requests1, data, cmddir
    title = "登录"
    log("info", title, "请输入账号和密码")
    username = input("账号: ")
    password = getpass.getpass("密码: ")
    log("info", title, "正在登录中......")
    try:
        requests1 = requests.post(url=login, json={"username": username, "password": password}, headers=headers)
        post1 = json.loads(requests1.text)
    except:
        log("error", title, "登录失败, 请检查 config.ini 文件! 文件位于: " + cmddir)
        log("error", title, "错误信息:")
        log("error", title, requests1.text)
        post_login()
    else:
        if post1["data"] == "Succeeded":
            log("info", title, "登录成功")
        else:
            log("error", title, "登录失败, 请检查 config.ini 文件! 文件位于: " + cmddir)
            log("error", title, post1["error"])
            log("error", title, post1["data"])
            post_login()

#获取 cookies
def get_cookies():
    global config, cookie, cmddir, requests1
    post_login()
    cookies = requests.utils.dict_from_cookiejar(requests1.cookies)
    csrftoken = cookies["csrftoken"]
    sessionid = cookies["sessionid"]
    cookie = "csrftoken=" + csrftoken + ";sessionid=" + sessionid
    #写入cookie到文件
    config.set("config", "cookies", cookie)
    with open(cmddir, "w", encoding="utf-8") as cookies :
        config.write(cookies)
        log("info", "登录", "获取 cookie 成功!")

#检查 cookies
def check_cookies():
    global headers1, get2, cookie, userinfo
    if cookie == "":
        log("error", "登录", "未检测到 cookies 文件, 尝试重新获取......")
        get_cookies()
        check_cookies()
    else:
        log("info", "登录", "已检测到 cookies 文件, 尝试直接登录......")
        #头文件
        headers1 = {
            "Content-Type": "application/json;charset=utf-8",
            "Cookie": cookie,
            "X-CSRFToken": cookie[10 : 74]
        }
        try:
            requests2 = requests.get(url=userinfo, headers=headers1)
            get2 = json.loads(requests2.text)
            name = get2["data"]["user"]["username"]
        except :
            get_cookies()
            check_cookies()

#获取用户信息
def get_info():
    global error,get2
    title = "用户信息"
    log("info", title, "正在获取用户信息......")
    if get2["data"] :
        log("info", title, "获取成功!")
        log("info", title, "数据id: " + str(get2["data"]["id"]))
        log("info", title, "用户id: " + str(get2["data"]["user"]["id"]))
        log("info", title, "用户名: " + str(get2["data"]["user"]["username"]))
        log("info", title, "邮箱: " + str(get2["data"]["user"]["email"]))
        log("info", title, "用户组: " + str(get2["data"]["user"]["admin_type"]))
        log("info", title, "问题权限: " + str(get2["data"]["user"]["problem_permission"]))
        log("info", title, "注册时间: " + get2["data"]["user"]["create_time"][:10] + get2["data"]["user"]["create_time"][11:19])
        log("info", title, "最后登录时间: " + get2["data"]["user"]["last_login"][:10] + get2["data"]["user"]["last_login"][11:19])
        log("info", title, "两步验证: " + str(get2["data"]["user"]["two_factor_auth"]))
        log("info", title, "api是否开放: " + str(get2["data"]["user"]["open_api"]))
        log("info", title, "是否被禁用: " + str(get2["data"]["user"]["is_disabled"]))
        log("info", title, "真实姓名: " + str(get2["data"]["real_name"]))
        log("info", title, "ACM问题状态: " + str(get2["data"]["acm_problems_status"]))
        log("info", title, "OI问题状态: " + str(get2["data"]["oi_problems_status"]))
        log("info", title, "头像地址: " + str(get2["data"]["avatar"]))
        log("info", title, "博客: " + str(get2["data"]["blog"]))
        log("info", title, "心情: " + str(get2["data"]["mood"]))
        log("info", title, "github地址: " + str(get2["data"]["github"]))
        log("info", title, "学校: " + str(get2["data"]["school"]))
        log("info", title, "major: " + str(get2["data"]["major"]))
        log("info", title, "语言: " + str(get2["data"]["language"]))
        log("info", title, "年级: " + str(get2["data"]["grade"]))
        log("info", title, "AC题数: " + str(get2["data"]["accepted_number"]))
        log("info", title, "总成绩: " + str(get2["data"]["total_score"]))
        log("info", title, "提交编号: " + str(get2["data"]["submission_number"]))
        log("info", title, "稳点: " + str(get2["data"]["experience"]))
        log("info", title, "当前等级: " + get_level())
    else:
        get_cookies()
        check_cookies()

#用 get 方法获取签到状态
def get_sign():
    global requests3, get3, error
    title = "签到"
    requests3 = requests.get(url=sighin, headers=headers1)
    get3 = json.loads(requests3.text)
    log("info", title, "查询签到状态中......")
    if get3["data"] :
        if get3["data"]["sighinstatus"] == "true":
            sighinstatus="已登录"
        elif get3["data"]["sighinstatus"] == "false":
            sighinstatus="未登录"
        log("info", title, "连续签到天数 : " + str(get3["data"]["continue_sighin_days"]))
        log("info", title, "最后签到时间 : " + str(get3["data"]["last_sighin_time"]))
        log("info", title, "登录状态 : " + sighinstatus)
    else:
        get_cookies()
        check_cookies()

#用 post 方法实现签到
def post_sign():
    title = "签到"
    global requests4, post4
    print("\033[0;30m++++++++++++++++++++++++++++++++\033[1;34m[签到]\033[0m")
    requests4 = requests.post(url=sighin, headers=headers1)
    post4 = json.loads(requests4.text)
    if post4["data"] == "Singined":
        log("info", title, "稳健佬, 您已经签过到了呀~明天再来哦")
    elif post4["data"]["info"] == "Success":
        log("info", title, "签到成功!")
        log("info", title, "获得稳点 : " + str(post4["data"]["experience"]))
        log("info", title, "当前等级 : " + get_level())
    else:
        get_cookies()
        check_cookies()

#计算等级
def get_level():
    level = int(json.dumps(get2["data"]["experience"]))
    if level >= 0 and level <= 99 : level = "\033[1;46m小白兔\033[0m"
    elif level >= 100 and level <= 199 : level = "\033[1;44m菜鸟\033[0m"
    elif level >= 200 and level <= 499 : level = "\033[1;45m键盘虾\033[0m"
    elif level >= 500 and level <= 999 : level = "\033[1;42m马农\033[0m"
    elif level >= 1000 and level <= 4999 : level = "\033[1;43m牛人\033[0m"
    elif level >= 5000 and level <= 9999 : level ="\033[1;41m程序猿\033[0m"
    else: level = "\033[1;40m攻城狮\033[0m"
    return level

limit = 20
page = 1
def problem_list():
    global get5, limit, page, problem_id
    title = "题目列表"
    print("\033[0;30m++++++++++++++++++++++++++++++\033[1;34m[题目]\033[0m")
    offset = (page - 1)*20
    requests5 = requests.get(url=gt_problem+"&offset="+str(offset)+"&limit="+str(limit), headers=headers1)
    get5 = json.loads(requests5.text)
    problem_detail = prettytable.PrettyTable(["状态", "题号", "题目", "难度", "提交总数", "通过率"])
    total = get5["data"]["total"]
    if limit > total :
        limit = total
    if total % 20 > 0 :
        total = total // 20 + 1
    else:
        total //= 20
    titlelist = {}
    for n1 in range(limit):
        _id = get5["data"]["results"][n1]["_id"]
        my_status = get5["data"]["results"][n1]["my_status"]
        titlelist[_id] = n1
        title1 = get5["data"]["results"][n1]["title"]
        difficulty = get5["data"]["results"][n1]["difficulty"]
        submission_number = get5["data"]["results"][n1]["submission_number"]
        accepted_number = get5["data"]["results"][n1]["accepted_number"]
        if submission_number == 0 :
            acv = "0%"
        else:
            acv = str(int(accepted_number)/int(submission_number)*100)[ : 5]+"%"
        problem_detail.add_row([color(my_status), _id, title1, color(difficulty), submission_number, acv])
    log("info", title, "\n" + str(problem_detail))
    log("info", title, "                              第" + str(page) + "页 共" + str(total) + "页")
    log("info", title, "进入问题请输入题号")
    log("info", title, "menu         返回菜单")
    log("info", title, "page:页码     跳转指定页码")
    log("info", title, "cls          清屏")
    log("info", title, "exit         退出")
    while True :
        print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m", end="")
        into = input(">")
        if into == "menu":
            page = 1
            menu()
        elif into == "help":
            log("info", title, "进入问题请输入题号")
            log("info", title, "menu         返回菜单")
            log("info", title, "page:页码     跳转指定页码")
            log("info", title, "cls          清屏")
            log("info", title, "exit         退出")
        elif into == "exit":
            log("error", title, "正在退出!!")
            sys.exit()
        elif into == "cls":
            os.system("cls")
        elif len(into) > 5 and into[:5] == "page:" and into[5:].isdigit() and int(into[5:]) > 0 and int(into[5:]) <= total:
            page = int(into[5 : ])
            os.system("cls")
            problem_list()
        else:
            problem_id = titlelist.get(into, "None")
            if problem_id != "None": problem_info()
            else: log("error", title, "输入错误, 请重新输入")

def problem_info():
    global get5, page, problem_id
    title = "题目详细"
    print("\033[0;30m++++++++++++++++++++++++++++++\033[1;34m[题目详细]\033[0m")
    log("info", title, "\033[1;34;47m题目: \033[0m\n"+get5["data"]["results"][problem_id]["title"])
    log("info", title, "\033[1;34;47m描述: \033[0m\n"+get5["data"]["results"][problem_id]["description"][3:-4])
    log("info", title, "\033[1;34;47m输入: \033[0m\n"+get5["data"]["results"][problem_id]["input_description"][3:-4])
    log("info", title, "\033[1;34;47m输出: \033[0m\n"+get5["data"]["results"][problem_id]["output_description"][3:-4])
    samples_id = 0
    while True :
        try:
            log("info", title, "\033[1;34;47m输入样例" + str(samples_id + 1) + ":\033[0m\n" + str(get5["data"]["results"][problem_id]["samples"][samples_id]["input"]))
            log("info", title, "\033[1;34;47m输出样例" + str(samples_id + 1) +":\033[0m\n{}" + str(get5["data"]["results"][problem_id]["samples"][samples_id]["output"]))
            samples_id += 1
        except: 
            break
    log("info", title, "\033[1;34;47m提示: \033[0m\n" + str(get5["data"]["results"][problem_id]["hint"][3:-4]))
    log("info", title, "\033[1;34;47m来源: \033[0m" + str(get5["data"]["results"][problem_id]["source"]))
    log("info", title, "\033[1;34;47m统计: \033[0m")
    for x1 in range(-2, 8):
        try:
            log("info", title, color(x1) + ": " + str(get5["data"]["results"][problem_id]["statistic_info"][str(x1)]))
        except:
            continue
    log("info", title, "post     提交")
    log("info", title, "back     返回问题列表")
    log("info", title, "menu     返回菜单")
    log("info", title, "cls      清屏")
    log("info", title, "exit     退出")
    while True :
        print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m", end="")
        into = input(">")
        if into == "menu":
            page = 1
            menu()
        if into == "help":
            log("info", title, "post     提交")
            log("info", title, "back     返回问题列表")
            log("info", title, "menu     返回菜单")
            log("info", title, "cls      清屏")
            log("info", title, "exit     退出")
        elif into == "exit":
            log("error", title, "正在退出!!")
            sys.exit()
        elif into == "back":
            problem_list()
        elif into == "post":
            post_problem()
        elif into == "cls":
            os.system("cls")
        else:
            title = "题目详细"
            log("error", title, "输入错误, 请重新输入")

def post_problem():
    global get5, problem_id
    title = "提交代码"
    id = get5["data"]["results"][problem_id]["id"]
    languages = get5["data"]["results"][problem_id]["languages"]
    try :
        with open("code.txt", mode="r", encoding="utf-8") as code:
            codes = code.read()
    except :
        log("error", title, "未找到 code.txt, 正在创建......")
        with open("code", mode="w", encoding="utf-8"):
            log("info", title, "创建成功!")
    b = input("已找到 code.txt 文件, 是(Y)否(N)使用?默认Y: ")
    if b != "Y" and b != "":
        problem_info()
    log("info", title, "提交语言可选: ")
    for x1 in languages: 
        print('"'+x1+'", ', end="")
    into = input("\n请输入提交语言, 默认 C++: ")
    if into in languages :
        language = into
        log("info", title, "已选择: "+language)
    else:
        language = "C++"
        log("info", title, "已选择: "+language)
    log("info", title, "正在提交中.....")
    data1 = {"problem_id": id, "language": language, "code": codes}
    requests6 = requests.post(url=tj_problem, json=data1, headers=headers1)
    post6 = json.loads(requests6.text)
    try:
        submission_id = post6["data"]["submission_id"]
        submission(post6["data"]["submission_id"])
    except:
        log("error", title, post6["data"])
        problem_info()

def submission(submission_id):
    title = "提交结果"
    requests7 = requests.get(url=tj_problem+submission_id, headers=headers1)
    get7 = json.loads(requests7.text)
    log("info", title, "提交状态 : "+color(get7["data"]["result"]))
    if get7["data"]["result"] == 6 or get7["data"]["result"] == 7 :
        log("info", title, "查询状态中......")
        time.sleep(3)
        submission(submission_id)
    else:
        print("\033[0;30m++++++++++++++++++++++++++++++\033[1;34m[提交结果]\033[0m")
        log("info", title, "提交状态: "+color(get7["data"]["result"]))
        if get7["data"]["result"] == -2 or get7["data"]["result"] == 5 :
            log("error", title, "错误信息: " + get7["data"]["statistic_info"]["err_info"])
        else:
            log("info", title, "时间: " + str(get7["data"]["statistic_info"]["time_cost"]) + "ms   内存: " + str(get7["data"]["statistic_info"]["memory_cost"]//1048576) + "MB   语言: " + get7["data"]["language"] + "   提交者: " + str(get7["data"]["username"]))
            log("info", title, "各个评测点状态: \n")
            submission_list = prettytable.PrettyTable(["ID", "状态", "内存", "CPU用时", "真实时间", "分数", "返回值"])
            id = 0
            while True :
                try :
                    result = color(get7["data"]["info"]["data"][id]["result"])
                    memory = str(get7["data"]["info"]["data"][id]["memory"]//1048576)+"MB"
                    cpu_time = str(get7["data"]["info"]["data"][id]["cpu_time"])+"ms"
                    real_time = str(get7["data"]["info"]["data"][id]["real_time"])+"ms"
                    signal= get7["data"]["info"]["data"][id]["signal"]
                    exit_code = get7["data"]["info"]["data"][id]["exit_code"]
                    id += 1
                    submission_list.add_row([id, result, memory, cpu_time, real_time, signal, exit_code])
                except:
                    break
            log("info", title, submission_list)
        log("info", title, "提交id: " + str(get7["data"]["id"]))
        log("info", title, "提交时间: " + str(get7["data"]["create_time"][ : 10]+get7["data"]["create_time"][11:19]))
        log("info", title, "提交ip: " + str(get7["data"]["ip"]))
        log("info", title, "代码: \n" + str(get7["data"]["code"]))
        log("info", title, "分享状态: " + str(get7["data"]["shared"]))
        log("info", title, "\nchange         切换分享状态")
        log("info", title, "problem_info   返回问题详细")
        log("info", title, "problem_list   返回问题列表")
        log("info", title, "menu           返回菜单")
        log("info", title, "cls            清屏")
        log("info", title, "exit           退出")
        while True :
            print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m", end="")
            into = input(">")
            if into == "menu":
                page = 1
                menu()
            elif into == "exit":
                log("error", title, "正在退出!!")
                sys.exit()
            elif into == "help":
                log("info", title, "change         切换分享状态")
                log("info", title, "problem_info   返回问题详细")
                log("info", title, "problem_list   返回问题列表")
                log("info", title, "menu           返回菜单")
                log("info", title, "cls            清屏")
                log("info", title, "exit           退出")
            elif into == "cls":
                os.system("cls")
            elif into == "change":
                if get7["data"]["shared"]: 
                    data2 = {"id": submission_id, "shared": False}
                else: 
                    data2 = {"id": submission_id, "shared": True}
                requests8 = requests.put(url=tj_problem, data=data2, headers=headers1)
                requests7 = requests.get(url=tj_problem+submission_id, headers=headers1)
                get7 = json.loads(requests7.text)
                print(get7)
                print(requests8)
                print(requests8.text)
                print(json.loads(requests8.text))
                log("info", title, "当前分享状态: " + str(get7["data"]["shared"]))
            elif into == "problem_info":
                problem_info()
            elif into == "problem_list":
                problem_list()
            else:
                log("error", title, "输入错误, 请重新输入")

if __name__ == '__main__':
    #主菜单
    menu()
