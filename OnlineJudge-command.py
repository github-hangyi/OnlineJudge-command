# -*- coding:utf-8 -*-
#导入库
import requests,json,os,time,getpass,prettytable,colorama,configparser
colorama.init()

#获取时间
def localtime_info():
    localtime = "\033[0;33m["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]\033[1;34m[info]\033[0m"
    return localtime

def localtime_error():
    localtime = "\033[0;33m["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]\033[1;31m[error]\033[0m"
    return localtime

headers = {"Content-Type":"application/json;charset=utf-8",
    "Cookie":"csrftoken=dvTfFYvCObIY7toKDE3NQI2PicjSo7Pisub1wuRhwLHBHODSbjJjWRw103eVeK6T",
    "X-CSRFToken": "dvTfFYvCObIY7toKDE3NQI2PicjSo7Pisub1wuRhwLHBHODSbjJjWRw103eVeK6T",
    "Connection":"close"
    }
dir = os.getcwd()
config = configparser.RawConfigParser()
config.read(dir+"\\config.ini")

if config.has_option("config","url") and config.has_option("config","auto_signin") and config.has_option("config","username") and config.has_option("config","password") and config.has_option("config","cookies"): error = 0
else:
    print("config.ini 文件出错,正在重新创建......")
    config.add_section("config")
    config["config"] = {"url":"",
    "auto_signin":"0",
    "username":"",
    "password":"",
    "cookies":"",
    }
    with open("config.ini","w",encoding="utf-8") as configfile: config.write(configfile)
if config["config"]["url"] != "" and config["config"]["auto_signin"] != "" and config["config"]["username"] != "" and config["config"]["password"] != "":
    url = config["config"]["url"]
    cookie = config["config"]["cookies"]
    auto_signin = config["config"]["auto_signin"]
    username = config["config"]["username"]
    password = config["config"]["password"]
else:
    print(localtime_error()+"!!!!!!请先配置 config.ini!!!!!!")
    exit()
cookie = config["config"]["cookies"]
#错误
error = 0
#登录地址
login = url+"/api/login"
#用户信息地址
info = url+"/api/profile"
#签到地址
sighin = url+"/api/sighin"
#获取问题地址
gt_problem = url+"/api/problem?"
tj_problem = url+"/api/submission?id="
#获取公告地址
announcement = url+"/api/announcement?offset=0&limit=10"

#主菜单
def menu():
    global error,get2
    if auto_signin == 1:
        print(localtime_info()+"自动签到模式已开启")
        get_sign()
        post_sign()
        exit()
    else: print(localtime_info()+"自动签到模式已关闭")
    print(localtime_info()+"欢迎来到主菜单,请输入指令,查看帮助请输 help")
    while True:
        print("\033[0;30m++++++++++++++++++++++++++++++++++\033[1;34m[menu]\033[0m")
        if error == 1: into = input("游客>")
        else:
            print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m",end="")
            into = input(">")
        if into == "help":
            print("帮助中心:")
            print("cookie     重新获取 cookie")
            print("info       获取基本信息")
            print("problem    题目列表")
            print("signin     签到")
            print("exit       退出")
            print("cls        清屏\n")
        elif into == "cookie":
            get_cookies()
            check_cookies()
        elif into == "info":
            os.system("cls")
            get_info()
        elif into == "signin":
            os.system("cls")
            get_sign()
            post_sign()
        elif into == "problem":
            os.system("cls")
            problem_list()
        elif into == "cls": os.system("cls")
        elif into == "exit": exit()
        else: print(localtime_error()+"输入无效,请重新输入")

#获取用户名和密码
def get_username_password():
    global data,error,username,password
    if username != "" and password != "" and error == 0: data = {"username":username,"password":password}
    else:
        print(localtime_error()+"请输入账号和密码")
        username = input("账号:")
        password = getpass.getpass("密码:")
        if name != "" and word != "":
            error = 0
            config.set("config","username",username)
            config.set("config","password",password)
            with open("config.ini", mode="w",encoding="utf-8") as userword: config.write(userword)
        else:
            print(localtime_error()+"输入错误!请重新输入\n")
            error = 1
            get_username_password()

#登录
def post_login():
    global requests1,error,data
    get_username_password()
    print(localtime_info()+"正在登录中......")
    try:
        requests1 = requests.post(url=login,json=data,headers=headers)
        post1 = json.loads(requests1.text)
    except:
        print(localtime_error()+"登录失败,请检查 config.ini 文件")
        exit()
    if post1["data"] == "Succeeded": print(localtime_info()+"登录成功")
    else:
        print(localtime_error(),end = "")
        into = input("登录失败,是(Y)否(N)否重新获取 cookies？默认是(Y):")
        if into == "Y" or into == "":
            post_login()
            get_cookies()
            check_cookies()
        else:exit()

#检查 cookies
def check_cookies():
    global headers1,get2,cookie
    if cookie == "":
        print(localtime_error()+"未检测到 cookies 文件,尝试重新获取......")
        get_cookies()
        check_cookies()
    else:
        print(localtime_info()+"已检测到 cookies 文件,尝试直接登录......")
        #头文件
        headers1 = {
            "Content-Type":"application/json;charset=utf-8",
            "Cookie":cookie,
            "X-CSRFToken":cookie[10:74],
            "Connection":"close"
        }
        requests2 = requests.get(url=info,headers=headers1)
        get2 = json.loads(requests2.text)
        try: name = get2["data"]["user"]["username"]
        except:
            print(localtime_error(),end = "")
            into = input("登录失败,是(Y)否(N)否重新获取 cookies？默认是(Y):")
            if into == "Y" or into == "":
                get_cookies()
                check_cookies()
            else:exit()

#获取 cookies
def get_cookies():
    global config,dir,cookie
    post_login()
    cookies = requests.utils.dict_from_cookiejar(requests1.cookies)
    csrftoken = cookies["csrftoken"]
    sessionid = cookies["sessionid"]
    cookie = "csrftoken="+csrftoken+";sessionid="+sessionid
    #写入cookie到文件
    config.set("config","cookies",cookie)
    with open("config.ini","w",encoding="utf-8") as cookies:
        config.write(cookies)
        print(localtime_info()+"获取 cookie 成功!")

#获取用户信息
def get_info():
    global error
    print("\033[0;30m++++++++++++++++++++++++++++++++++\033[1;34m[info]\033[0m")
    print(localtime_info()+"正在获取用户信息......")
    if get2["data"]:
        print(localtime_info()+"获取成功!")
        print(localtime_info()+"数据id:",get2["data"]["id"])
        print(localtime_info()+"用户id:",get2["data"]["user"]["id"])
        print(localtime_info()+"用户名:",get2["data"]["user"]["username"])
        print(localtime_info()+"邮箱:",get2["data"]["user"]["email"])
        print(localtime_info()+"用户组:",get2["data"]["user"]["admin_type"])
        print(localtime_info()+"问题权限:",get2["data"]["user"]["problem_permission"])
        print(localtime_info()+"注册时间:",get2["data"]["user"]["create_time"][:10],get2["data"]["user"]["create_time"][11:19])
        print(localtime_info()+"最后登录时间:",get2["data"]["user"]["last_login"][:10],get2["data"]["user"]["last_login"][11:19])
        print(localtime_info()+"两步验证:",get2["data"]["user"]["two_factor_auth"])
        print(localtime_info()+"api是否开放:",get2["data"]["user"]["open_api"])
        print(localtime_info()+"是否不可用:",get2["data"]["user"]["is_disabled"])
        print(localtime_info()+"真实姓名:",get2["data"]["real_name"])
        #print(localtime_info()+"ACM问题状态:",get2["data"]["acm_problems_status"])
        #print(localtime_info()+"OI问题状态:",get2["data"]["oi_problems_status"])
        print(localtime_info()+"头像地址:",get2["data"]["avatar"])
        print(localtime_info()+"博客:",get2["data"]["blog"])
        print(localtime_info()+"心情:",get2["data"]["mood"])
        print(localtime_info()+"github:",get2["data"]["github"])
        print(localtime_info()+"学校:",get2["data"]["school"])
        print(localtime_info()+"major:",get2["data"]["major"])
        print(localtime_info()+"语言:",get2["data"]["language"])
        print(localtime_info()+"年级:",get2["data"]["grade"])
        print(localtime_info()+"稳点:",get2["data"]["experience"])
        print(localtime_info()+"当前等级:",get_level())
        print(localtime_info()+"AC题数:",get2["data"]["accepted_number"])
        print(localtime_info()+"总成绩:",get2["data"]["total_score"])
        print(localtime_info()+"提交编号:",get2["data"]["submission_number"])
    else:
        print(localtime_error(),end = "")
        into = input("获取失败,是(Y)否(N)否重新获取 cookies？默认是(Y):")
        if into == "Y" or into == "":
            get_cookies()
            check_cookies()
        else:exit()

#用 get 方法获取签到状态
def get_sign():
    global requests3,get3,error
    print("\033[0;30m++++++++++++++++++++++++++++++++\033[1;34m[signin]\033[0m")
    requests3 = requests.get(url=sighin,headers=headers1)
    get3 = json.loads(requests3.text)
    print(localtime_info()+"查询签到状态中......")
    if get3["data"]:
        if get3["data"]["sighinstatus"] == "true":
            sighinstatus="已登录"
        elif get3["data"]["sighinstatus"] == "false":
            sighinstatus="未登录"
        print(localtime_info()+"连续签到天数:",get3["data"]["continue_sighin_days"])
        print(localtime_info()+"最后签到时间:",get3["data"]["last_sighin_time"])
        print(localtime_info()+"登录状态:",sighinstatus)
    else:
        print(localtime_error(),end = "")
        into = input("获取失败,是(Y)否(N)否重新获取 cookies？默认是(Y):")
        if into == "Y" or into == "":
            get_cookies()
            check_cookies()
        else:exit()

#计算等级
def get_level():
    level = int(json.dumps(get2["data"]["experience"]))
    if level >= 0 and level <= 99: level = "\033[1;46m小白兔\033[0m"
    elif level >= 100 and level <= 199: level = "\033[1;44m菜鸟\033[0m"
    elif level >= 200 and level <= 499: level = "\033[1;45m键盘虾\033[0m"
    elif level >= 500 and level <= 999: level = "\033[1;42m马农\033[0m"
    elif level >= 1000 and level <= 4999: level = "\033[1;43m牛人\033[0m"
    elif level >= 5000 and level <= 9999: level ="\033[1;41m程序猿\033[0m"
    else: level = "\033[1;40m攻城狮\033[0m"
    return level

#用 post 方法实现签到
def post_sign():
    global requests4,post4,error
    requests4 = requests.post(url=sighin,headers=headers1)
    post4 = json.loads(requests4.text)
    if post4["data"] == "Singined":
        print(localtime_info()+"稳健佬,您已经签过到了呀~明天再来哦")
    elif post4["data"]["info"] == "Success":
        print(localtime_info()+"签到成功！")
        print(localtime_info()+"获得稳点:",post4["data"]["experience"])
        print(localtime_info()+"当前等级:",get_level())
    else:
        print(localtime_error(),end = "")
        into = input("获取失败,是(Y)否(N)否重新获取 cookies？默认是(Y):")
        if into == "Y" or into == "":
            get_cookies()
            check_cookies()
        else:exit()

limit = 20
page = 1
def problem_list():
    global get5,limit,page,problem_id
    print("\033[0;30m++++++++++++++++++++++++++++++\033[1;34m[problem list]\033[0m")
    offset = (page - 1) *20
    requests5 = requests.get(url=gt_problem+"&offset="+str(offset)+"&limit="+str(limit),headers=headers1)
    get5 = json.loads(requests5.text)
    problem_list = prettytable.PrettyTable(["状态","题号","题目","难度","总数","通过率"])
    total = get5["data"]["total"]
    if limit > total: limit = total
    if total % 20 > 0: total = total // 20 + 1
    else: total //= 20
    titlelist = {}
    for n1 in range(limit):
        _id = get5["data"]["results"][n1]["_id"]
        my_status = get5["data"]["results"][n1]["my_status"]
        titlelist[_id] = n1
        title = get5["data"]["results"][n1]["title"]
        difficulty = get5["data"]["results"][n1]["difficulty"]
        submission_number = get5["data"]["results"][n1]["submission_number"]
        accepted_number = get5["data"]["results"][n1]["accepted_number"]
        if submission_number == 0: acv = "0%"
        else: acv = str(int(accepted_number)/int(submission_number)*100)[:5]+"%"
        problem_list.add_row([color(my_status),_id,title,color(difficulty),submission_number,acv])
    print(problem_list)
    print("                              第{}页 共{}页".format(page,total))
    print(localtime_info()+"进入问题请输入题号,返回菜单(menu),跳转指定页码(page:页码),退出(exit)")
    while True:
        print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m",end="")
        into = input(">")
        if into == "menu":
            page = 1
            menu()
        elif into == "help": print(localtime_info()+"\n进入问题请输入题号\nmenu     返回菜单\npage:     页码跳转指定页码\ncls     清屏\nexit     退出")
        elif into == "exit": exit()
        elif into == "cls": os.system("cls")
        elif len(into) > 5 and into[:5] == "page:" and into[5:].isdigit() and int(into[5:]) > 0 and int(into[5:]) <= total:
            page = int(into[5:])
            os.system("cls")
            problem_list()
        else:
            problem_id = titlelist.get(into,"None")
            if problem_id != "None": problem_info()
            else: print(localtime_error()+"输入错误,请重新输入")

def problem_info():
    global get5,page,problem_id
    print("\033[0;30m++++++++++++++++++++++++++++++\033[1;34m[problem info]\033[0m")
    print("\033[1;34m题目:\033[0m\n"+get5["data"]["results"][problem_id]["title"])
    print("\033[1;34m描述:\033[0m\n"+get5["data"]["results"][problem_id]["description"][3:-4])
    print("\033[1;34m输入:\033[0m\n"+get5["data"]["results"][problem_id]["input_description"][3:-4])
    print("\033[1;34m输出:\033[0m\n"+get5["data"]["results"][problem_id]["output_description"][3:-4])
    samples_id = 0
    while True:
        try:
            samples_input = get5["data"]["results"][problem_id]["samples"][samples_id]["input"]
            samples_output = get5["data"]["results"][problem_id]["samples"][samples_id]["output"]
            print("\033[1;34m输入样例{}:\033[0m\n{}".format(samples_id + 1,samples_input))
            print("\033[1;34m输出样例{}:\033[0m\n{}".format(samples_id + 1,samples_output))
            samples_id += 1
        except: break
    print("\033[1;34m提示:\033[0m\n"+get5["data"]["results"][problem_id]["hint"][3:-4])
    print("\033[1;34m来源:\033[0m"+get5["data"]["results"][problem_id]["source"])
    print("\033[1;34m统计:\033[0m",end="")
    for x1 in range(-2,8):
        try: print(color(x1)+":",get5["data"]["results"][problem_id]["statistic_info"][str(x1)]+" ",end="")
        except: continue
    print("\n")
    while True:
        print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m",end="")
        into = input(">")
        if into == "menu":
            page = 1
            menu()
        if into == "help": print(localtime_info()+"\npost     提交\nback     返回问题列表\nmenu     返回菜单\ncls     清屏\nexit     退出")
        elif into == "exit": exit()
        elif into == "back": problem_list()
        elif into == "post": post_problem()
        elif into == "cls": os.system("cls")
        else:print(localtime_error()+"输入错误,请重新输入")

def post_problem():
    global get5,problem_id
    id = get5["data"]["results"][problem_id]["id"]
    languages = get5["data"]["results"][problem_id]["languages"]
    print(localtime_info()+"提交语言可选:",end="")
    for x1 in languages: print('"'+x1+'" ',end="")
    print("\n"+localtime_info(),end="")
    into = input("请输入提交语言,默认 C++:")
    if into in languages:
        language = into
        print(localtime_info()+"已选择:",language)
    else:
        language = "C++"
        print(localtime_info()+"已选择:",language)
    try:
        with open("code.cpp",mode="r",encoding="utf-8") as code:
            print(localtime_info(),end="")
            b = input("已找到 code.cpp,是(Y)否(N)使用?默认Y:")
            if b == "N": problem_info()
            else: codes = code.read()
    except:
        print(localtime_error()+"未找到 code.cpp,正在创建......")
        with open("code.cpp", mode="w",encoding="utf-8"): print(localtime_info()+"创建成功!")
        post_problem()
    data1 = {"problem_id":id,"language":language,"code":codes}
    requests6 = requests.post(url=tj_problem,json=data1,headers=headers1)
    post6 = json.loads(requests6.text)
    submission_id = post6["data"]["submission_id"]
    submission(submission_id)

def submission(submission_id):
    requests7 = requests.get(url=tj_problem+submission_id,headers=headers1)
    get7 = json.loads(requests7.text)
    print("提交状态:",color(get7["data"]["result"]))
    if get7["data"]["result"] == 6 or get7["data"]["result"] == 7:
        print(localtime_info()+"查询状态中......")
        time.sleep(3)
        submission(submission_id)
    else:
        os.system("cls")
        print("\033[0;30m++++++++++++++++++++++++++++++\033[1;34m[submission]\033[0m")
        print("提交状态:",color(get7["data"]["result"]))
        if get7["data"]["result"] == -2 or get7["data"]["result"] == 5:
            print(get7["data"]["result"])
            print(localtime_error()+"错误信息:",get7["data"]["statistic_info"]["err_info"])
        else:
            print(localtime_info()+"时间:{}ms   内存:{}MB   语言:{}   提交者:{}".format(get7["data"]["statistic_info"]["time_cost"],get7["data"]["statistic_info"]["memory_cost"]//1048576,get7["data"]["language"],get7["data"]["username"]))
            print(localtime_info()+"各个评测点状态:")
            submission_list = prettytable.PrettyTable(["ID","状态","内存","CPU用时","真实时间","分数","返回值"])
            id = 0
            while True:
                try:
                    result = color(get7["data"]["info"]["data"][id]["result"])
                    memory = str(get7["data"]["info"]["data"][id]["memory"]//1048576)+"MB"
                    cpu_time = str(get7["data"]["info"]["data"][id]["cpu_time"])+"ms"
                    real_time = str(get7["data"]["info"]["data"][id]["real_time"])+"ms"
                    signal= get7["data"]["info"]["data"][id]["signal"]
                    exit_code = get7["data"]["info"]["data"][id]["exit_code"]
                    id += 1
                    submission_list.add_row([id,result,memory,cpu_time,real_time,signal,exit_code])
                except:break
            print(submission_list)
        print("提交id:",get7["data"]["id"])
        print("提交时间:",get7["data"]["create_time"][:10],get7["data"]["create_time"][11:19])
        print("代码:\n"+get7["data"]["code"])
        print("分享状态:",get7["data"]["shared"])
        while True:
            print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m",end="")
            into = input(">")
            if into == "menu":
                page = 1
                menu()
            elif into == "exit": exit()
            elif into == "help":print(localtime_info()+"change     切换分享状态\nproblem_info 返回问题详细\nproblem_list  返回问题列表\nmenu     返回菜单\ncls       清屏\nexit     退出")
            elif into == "cls": os.system("cls")
            elif into == "change":
                if get7["data"]["shared"]: data2 = {"id":submission_id,"shared":False}
                else: data2 = {"id":submission_id,"shared":True}
                requests.put(url=tj_problem,data=data2,headers=headers1)
                requests7 = requests.get(url=tj_problem+submission_id,headers=headers1)
                get7 = json.loads(requests7.text)
                print(localtime_info()+"当前分享状态:",get7["data"]["shared"])
            elif into == "problem_info": problem_info()
            elif into == "problem_list": problem_list()
            else:print(localtime_error()+"输入错误,请重新输入")

def color(color):
    #####提交状态#####
    if color == -2 or color == "CE": color = "\033[1;35mCompile Error\033[0m"
    elif color == -1 or color == "WA": color = "\033[1;31mWrong Answer\033[0m"
    elif color == 0 or color == "AC": color = "\033[1;32mAccepted\033[0m"
    elif color == 1 or color == 2 or color == "TLE": color = "\033[1;31mTime Limit Exceeded\033[0m"
    elif color == 3 or color == "MLE": color = "\033[1;31mMemory Limit Exceeded\033[0m"
    elif color == 4 or color == "RE": color = "\033[1;31mRuntime Error\033[0m"
    elif color == 5 or color == "SE": color = "\033[1;31mSystem Error\033[0m"
    elif color == 6 or color == "Pending": color = "\033[1;36mPending\033[0m"
    elif color == 7 or color == "Judging": color = "\033[0;36mJudging\033[0m"
    elif color == 8 or color == "PAC": color = "\033[1;36mPartial Accepted\033[0m"
    #####难度#####
    elif color == "High": color = "\033[1;41m 高 \033[0m"
    elif color == "Mid": color = "\033[1;44m 中 \033[0m"
    elif color == "Low": color = "\033[1;42m 低 \033[0m"
    else : color = "-"
    return color

if __name__ == '__main__':
    print(localtime_info()+"有错误一般都是 cookie 错误,尝试重新获取 cookies 一般都可解决")
    #检查 cookie文件是否存在
    check_cookies()
    #主菜单
    menu()
