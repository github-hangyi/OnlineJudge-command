## 一个[青岛 OnlineJudge](https://github.com/QingdaoU/OnlineJudge)的命令行版！

## 功能

- [x] 登录
- [x] 自动签到
- [x] 获取基本信息
- [x] 做题(部分题目显示有问题）
- [x] 日志

### TODO

- [ ] 公告
- [ ] 比赛
- [ ] 提交
- [ ] 状态
- [ ] 公告
- [ ] 排名
- [ ] 在线 IDE
- [ ] 关于

## 使用教程

- ### 安装

1. 下载此代码
2. 首次使用请自行安装 Python3 和 pip 并执行以下命令

```
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 运行

```
python OnlineJudge-command.py
```

- ### 配置文件介绍

|        项目         |            介绍             |
| :-----------------: | :-------------------------: |
|         url         |       必填，OJ 的地址       |
| auto_signin = False | 必填自动签到模式 True/False |
|       cookies       |          不用更改           |
|        ftqq         |     （可选）填方糖 KEY      |

## 帮助

- ## [主菜单]

```
帮助中心:
cookie    重新获取 cookie
info      获取基本信息
problem   题目列表
signin    签到
exit      退出
```

- ## [题目列表]

```
goto 题号      查看题号题目
search 题目    搜索题目
page 页码      跳转指定页码
return        返回
```

- ## [题目详细]

```
post          提交
return        返回
```

- ## [提交结果]

```
change        切换分享状态
return        返回
```
