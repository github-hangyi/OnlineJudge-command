# 警告！！！！！未完成，请勿下载
## 一个[青岛OnlineJudge](https://github.com/QingdaoU/OnlineJudge)的命令行版！
## 安装
1. 下载此代码
2. 首次使用请自行安装 Python 和 pip 并执行以下命令
```
pip install --upgrade pip
pip install -r requirements.txt
```
3. 运行
```
python OnlineJudge-command.py
```
## 使用教程
- ### 配置文件介绍
```
  [Config]
  #网站地址 !!!要加 http:// 或 https:// 末尾不用加 "/"!!!
  url = 
  #自动签到模式 = 1 为开，开启后无菜单界面，签到后自动退出
  auto_signin = 0
  #用户名
  username = 
  #密码 
  password = 
  #无需配置 
  cookies = 
```
- ##  主页面[menu]
```
$help
帮助中心:
cookie    重新获取 cookie
info      获取基本信息
problem   题目列表
signin    签到
cls       清屏
exit      退出
```
- ## 题目列表[problem list]
```
$help
进入问题请输入题号
menu     返回菜单
page:    页码跳转指定页码
cls      清屏
exit     退出
```
- ## 问题详细[problem info]
```
$help
post     提交
back     返回问题列表
menu     返回菜单
cls      清屏
exit     退出
```
- ## 提交状态[submission]
```
$help
change        切换分享状态
problem_info  返回问题详细
problem_list  返回问题列表
menu          返回菜单
cls           清屏
exit          退出 
```
