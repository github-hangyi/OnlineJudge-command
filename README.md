## 一个[青岛OnlineJudge](https://github.com/QingdaoU/OnlineJudge)的命令行版！

## 功能
- [x] 登录
- [x] 签到
- [x] 获取基本信息
- [x] 做题(部分题目显示有问题）
- [x] Log日志
- [ ] 比赛
- [ ] 查看已解决问题
- [ ] 查看状态
- [ ] 查看公告
- [ ] 查看排名
- [ ] 在线IDE
- [ ] 查看关于信息
- [ ] 设置基本信息

## 使用教程
- ### 安装
1. 下载此代码
2. 首次使用请自行安装 Python3 和 pip 并执行以下命令
```
pip3 install --upgrade pip3
pip3 install -r requirements.txt
```
3. 运行
```
python3 OnlineJudge-command.py
```
- ### 配置文件介绍
```
[Config]
#网站地址
url = https://www.example.com
#自动签到模式 = True为开，开启后无菜单界面，签到后自动退出
auto_signin = False
```
- ##  [主菜单]
```console
$help
帮助中心:
cookie    重新获取 cookie
info      获取基本信息
problem   题目列表
signin    签到
clear     清屏
exit      退出
```
- ## [题目列表]
```console
$help
进入问题请输入题号
menu     返回菜单
page:    页码跳转指定页码
clear    清屏
exit     退出
  ```
- ## [题目详细]
```console
$help
post     提交
back     返回问题列表
menu     返回菜单
clear    清屏
exit     退出
```
- ## [提交结果]
```console
$help
change        切换分享状态
problem_info  返回问题详细
problem_list  返回问题列表
menu          返回菜单
clear         清屏
exit          退出 
```
