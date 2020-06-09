# -*- coding:utf-8 -*-
#导入库
import requests,json,sys,logging,os,time,getpass,prettytable,colorama,configparser
colorama.init()

#log模块
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("log.log",encoding="utf-8")
ch = logging.StreamHandler()
fh.setFormatter(logging.Formatter(fmt="[%(asctime)s] [%(title)s] [%(levelname)s] [%(message)s]"))
ch.setFormatter(logging.Formatter(fmt="\033[0;33m[%(asctime)s] %(color)s[%(levelname)s]\033[0m [%(message)s]",datefmt="%X"))
logger.addHandler(fh)
logger.addHandler(ch)
logger.error("",extra={'title':'','color':color(error)})

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
cmddir = os.getcwd()
cmddir = cmddir+"\\config.ini"
config = configparser.RawConfigParser()
config.read(cmddir,encoding="utf-8")

if config.has_option("config","url") and config.has_option("config","auto_signin") and config.has_option("config","cookies"):error = 0
else:
    logger.error("config.ini 文件出错,正在重新创建......",extra={'title':'TITLE','color':color(error)})
    config.add_section("config")
    config["config"] = {"url":"","auto_signin":"0","cookies":""}
    with open(cmddir,"w",encoding="utf-8") as configfile: config.write(configfile)
    logger.info("创建成功! 文件位于: "+cmddir,extra={'title':'TITLE','color':color(info)})

if config["config"]["url"] != "" and config["config"]["auto_signin"] != "":
    url = config["config"]["url"]
    cookie = config["config"]["cookies"]
    auto_signin = config["config"]["auto_signin"]
else:
    logger.error("!!请先配置 config.ini!! 文件位于: "+cmddir,extra={'title':'TITLE','color':color(error)})
    os.system("pause")
    sys.exit()

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
    global error,get2,auto_signin
    #检查 cookie文件是否存在
    check_cookies()
    if auto_signin == "1":
        logger.info("自动签到模式已开启",extra={'title':'menu','color':color(info)})
        post_sign()
        get_sign()
        sys.exit()
    else: logger.info("自动签到模式已关闭",extra={'title':'menu','color':color(info)})
    logger.info("欢迎来到主菜单,请输入指令,查看帮助请输 help",extra={'title':'menu','color':color(info)})
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
            post_sign()
            get_sign()
        elif into == "problem":
            os.system("cls")
            problem_list()
        elif into == "cls": os.system("cls")
        elif into == "exit":
            logger.info("正在退出！！",extra={'title':'menu','color':color(info)})
            sys.exit()
        else: 
        logger.error("输入无效,请重新输入",extra={'title':'menu','color':color(error)})

#登录
def post_login():
    global requests1,data
    logger.info("请输入账号和密码",extra={'title':'post_login','color':color(info)})
    username = input("账号:")
    password = getpass.getpass("密码:")
    logger.info("正在登录中......",extra={'title':'post_login','color':color(info)})
    try:
        requests1 = requests.post(url=login,json={"username":username,"password":password},headers=headers)
        post1 = json.loads(requests1.text)
    except:
        logger.error("登录失败,请检查 config.ini 文件! 文件位于: "+cmddir,extra={'title':'post_login','color':color(error)})
        os.system("pause")
        sys.exit()
    else:
        if post1["data"] == "Succeeded": logger.info("登录成功",extra={'title':'post_login','color':color(info)})
        else:
            logger.error("登录失败,请检查 config.ini 文件! 文件位于: "+cmddir,extra={'title':'post_login','color':color(error)})
            os.system("pause")
            sys.exit()

#检查 cookies
def check_cookies():
    global headers1,get2,cookie
    if cookie == "":
        logger.error("未检测到 cookies 文件,尝试重新获取......",extra={'title':'check_cookies','color':color(error)})
        get_cookies()
        check_cookies()
    else:
        logger.info("已检测到 cookies 文件,尝试直接登录......",extra={'title':'check_cookies','color':color(info)})
        #头文件
        headers1 = {
            "Content-Type":"application/json;charset=utf-8",
            "Cookie":cookie,
            "X-CSRFToken":cookie[10:74]
        }
        requests2 = requests.get(url=info,headers=headers1)
        get2 = json.loads(requests2.text)
        try: name = get2["data"]["user"]["username"]
        except:
            get_cookies()
            check_cookies()

#获取 cookies
def get_cookies():
    global config,cookie,cmddir,requests1
    post_login()
    cookies = requests.utils.dict_from_cookiejar(requests1.cookies)
    csrftoken = cookies["csrftoken"]
    sessionid = cookies["sessionid"]
    cookie = "csrftoken="+csrftoken+";sessionid="+sessionid
    #写入cookie到文件
    config.set("config","cookies",cookie)
    with open(cmddir,"w",encoding="utf-8") as cookies:
        config.write(cookies)
        logger.info("获取 cookie 成功!",extra={'title':'get_cookies','color':color(info)})

#获取用户信息
def get_info():
    global error
    logger.info("[info]",extra={'title':'get_info','color':color(info)})
    logger.info("正在获取用户信息......",extra={'title':'get_info','color':color(info)})
    if get2["data"]:
        logger.info("",extra={'title':'get_info','color':color(info)})
        logger.info("获取成功!",extra={'title':'get_info','color':color(info)})
        logger.info("数据id:",get2["data"]["id"],extra={'title':'get_info','color':color(info)})
        logger.info("用户id:",get2["data"]["user"]["id"],extra={'title':'get_info','color':color(info)})
        logger.info("用户名:",get2["data"]["user"]["username"],extra={'title':'get_info','color':color(info)})
        logger.info("邮箱:",get2["data"]["user"]["email"],extra={'title':'get_info','color':color(info)})
        logger.info("用户组:",get2["data"]["user"]["admin_type"],extra={'title':'get_info','color':color(info)})
        logger.info("问题权限:",get2["data"]["user"]["problem_permission"],extra={'title':'get_info','color':color(info)})
        logger.info("注册时间:",get2["data"]["user"]["create_time"][:10],get2["data"]["user"]["create_time"][11:19],extra={'title':'get_info','color':color(info)})
        logger.info("最后登录时间:",get2["data"]["user"]["last_login"][:10],get2["data"]["user"]["last_login"][11:19],extra={'title':'get_info','color':color(info)})
        logger.info("两步验证:",get2["data"]["user"]["two_factor_auth"],extra={'title':'get_info','color':color(info)})
        logger.info("api是否开放:",get2["data"]["user"]["open_api"],extra={'title':'get_info','color':color(info)})
        logger.info("是否不可用:",get2["data"]["user"]["is_disabled"],extra={'title':'get_info','color':color(info)})
        logger.info("真实姓名:",get2["data"]["real_name"],extra={'title':'get_info','color':color(info)})
        #logger.info("ACM问题状态:",get2["data"]["acm_problems_status"],extra={'title':'get_info','color':color(info)})
        #logger.info("OI问题状态:",get2["data"]["oi_problems_status"],extra={'title':'get_info','color':color(info)})
        logger.info("头像地址:",get2["data"]["avatar"],extra={'title':'get_info','color':color(info)})
        logger.info("博客:",get2["data"]["blog"],extra={'title':'get_info','color':color(info)})
        logger.info("心情:",get2["data"]["mood"],extra={'title':'get_info','color':color(info)})
        logger.info("github:",get2["data"]["github"],extra={'title':'get_info','color':color(info)})
        logger.info("学校:",get2["data"]["school"],extra={'title':'get_info','color':color(info)})
        logger.info("major:",get2["data"]["major"],extra={'title':'get_info','color':color(info)})
        logger.info("语言:",get2["data"]["language"],extra={'title':'get_info','color':color(info)})
        logger.info("年级:",get2["data"]["grade"],extra={'title':'get_info','color':color(info)})
        logger.info("AC题数:",get2["data"]["accepted_number"],extra={'title':'get_info','color':color(info)})
        logger.info("总成绩:",get2["data"]["total_score"],extra={'title':'get_info','color':color(info)})
        logger.info("提交编号:",get2["data"]["submission_number"],extra={'title':'get_info','color':color(info)})
        logger.info("稳点:",get2["data"]["experience"],extra={'title':'get_info','color':color(info)})
        logger.info("当前等级:",get_level(),extra={'title':'get_info','color':color(info)})
    else:
        get_cookies()
        check_cookies()

#用 get 方法获取签到状态
def get_sign():
    global requests3,get3,error
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
        get_cookies()
        check_cookies()

#用 post 方法实现签到
def post_sign():
    global requests4,post4
    print("\033[0;30m++++++++++++++++++++++++++++++++\033[1;34m[signin]\033[0m")
    requests4 = requests.post(url=sighin,headers=headers1)
    post4 = json.loads(requests4.text)
    if post4["data"] == "Singined":
        print(localtime_info()+"稳健佬,您已经签过到了呀~明天再来哦")
    elif post4["data"]["info"] == "Success":
        print(localtime_info()+"签到成功！")
        print(localtime_info()+"获得稳点:",post4["data"]["experience"])
        print(localtime_info()+"当前等级:",get_level())
    else:
        get_cookies()
        check_cookies()

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

limit = 20
page = 1
def problem_list():
    global get5,limit,page,problem_id
    print("\033[0;30m++++++++++++++++++++++++++++++\033[1;34m[problem list]\033[0m")
    offset = (page - 1)*20
    requests5 = requests.get(url=gt_problem+"&offset="+str(offset)+"&limit="+str(limit),headers=headers1)
    get5 = json.loads(requests5.text)
    problem_detail = prettytable.PrettyTable(["状态","题号","题目","难度","总数","通过率"])
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
        problem_detail.add_row([color(my_status),_id,title,color(difficulty),submission_number,acv])
    print(problem_detail)
    print("                              第{}页 共{}页".format(page,total))
    print(localtime_info()+"进入问题请输入题号,返回菜单(menu),跳转指定页码(page:页码),退出(exit)")
    while True:
        print("\033[1;36m["+get2["data"]["user"]["username"]+"]\033[0m",end="")
        
        into = input(">")
        if into == "menu":
            page = 1
            menu()
        elif into == "help": print(localtime_info()+"\n进入问题请输入题号\nmenu     返回菜单\npage:     页码跳转指定页码\ncls     清屏\nexit     退出")
        elif into == "exit": 
            print(localtime_info()+"正在退出！！")
            sys.exit()
        elif into == "cls": os.system("cls")
        elif len(into) > 5 and into[:5] == "page:" and into[5:].isdigit() and int(into[5:]) > 0 and int(into[5:]) <= total:
            page = int(into[5:])
            os.system("cls")
            problem_list()
        else:
            problem_id = titlelist.get(into,"None")
            if problem_id != "None": problem_info()
            else: logger.error("输入错误,请重新输入",extra={'title':'problem_list','color':color(error)})

def problem_info():
    global get5,page,problem_id
    print("\033[0;31m++++++++++++++++++++++++++++++\033[1;34m[problem info]\033[0m")
    print("\033[1;34;47m题目:\033[0m\n"+get5["data"]["results"][problem_id]["title"])
    print("\033[1;34;47m描述:\033[0m\n"+get5["data"]["results"][problem_id]["description"][3:-4])
    
    print("\033[1;34;47m输入:\033[0m\n"+get5["data"]["results"][problem_id]["input_description"][3:-4])
    print("\033[1;34;47m输出:\033[0m\n"+get5["data"]["results"][problem_id]["output_description"][3:-4])
    samples_id = 0
    while True:
        try:
            samples_input = get5["data"]["results"][problem_id]["samples"][samples_id]["input"]
            samples_output = get5["data"]["results"][problem_id]["samples"][samples_id]["output"]
            print("\033[1;34;47m输入样例{}:\033[0m\n{}".format(samples_id + 1,samples_input))
            print("\033[1;34;47m输出样例{}:\033[0m\n{}".format(samples_id + 1,samples_output))
            samples_id += 1
        except: break
    print("\033[1;34;47m提示:\033[0m\n"+get5["data"]["results"][problem_id]["hint"][3:-4])
    print("\033[1;34;47m来源:\033[0m"+get5["data"]["results"][problem_id]["source"])
    print("\033[1;34;47m统计:\033[0m",end="")
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
        elif into == "exit": 
            print(localtime_info()+"正在退出！！")
            sys.exit()
        elif into == "back": problem_list()
        elif into == "post": post_problem()
        elif into == "cls": os.system("cls")
        else: logger.error("输入错误,请重新输入",extra={'title':'problem_list','color':color(error)})

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
        with open("code",mode="r",encoding="utf-8") as code:
            print(localtime_info(),end="")
            b = input("已找到 code,是(Y)否(N)使用?默认Y:")
            if b == "N": problem_info()
            else: codes = code.read()
    except:
        logger.error("未找到 code,正在创建......",extra={'title':'post_problem','color':color(error)})
        with open("code", mode="w",encoding="utf-8"): print(localtime_info()+"创建成功!")
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
            logger.info(get7["data"]["result"],extra={'title':'submission','color':color(info)})
            logger.error("错误信息:"+get7["data"]["statistic_info"]["err_info"],extra={'title':'submission','color':color(error)})
            
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
            elif into == "exit": 
                print(localtime_info()+"正在退出！！")
                sys.exit()
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
            else: logger.error("输入错误,请重新输入",extra={'title':'submission','color':color(error)})

def color(color):
    #####log日志#####
    if color == "info": color = '\033[1;34m'
    elif color == "error": color = '\033[1;31m'
    #####提交状态#####
    elif color == -2 or color == "CE": color = "\033[1;35mCompile Error\033[0m"
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
    #主菜单
    menu()
