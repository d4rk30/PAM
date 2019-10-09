# PAM
PAM（PockrAssetManagement 破壳资产管理工具）是一款面向白帽子的资产管理工具，它可以按照项目进行分类，提供目标站点的主域之后，后台可以实时+定期探测子域，并且在此基础上进行资产收集，包括如下信息：

- 域名
- IP
- 开放端口与服务
- Whois信息
- web指纹识别
- 相关漏洞提示
- ...



![](https://other-1256870184.cos.ap-beijing.myqcloud.com/2019-10-09-127.0.0.1_5000_project%20-1-.png)
![](https://other-1256870184.cos.ap-beijing.myqcloud.com/2019-10-09-127.0.0.1_5000_project_2.png)
## 开发进度
- [x] 数据库设计
- [x] 项目结构搭建
- [x] 项目管理
- [x] 主域管理
- [x] 子域管理与探测
- [ ] 获取IP与端口开放服务
- [ ] 获取Whois信息
- [ ] 后台目录扫描
- [ ] 获取指纹
- [ ] 定时任务
- [ ] 功能优化

## 后续计划
- 自动提交SRC，漏洞平台
- 威胁情报
- ...

## 部署方法
### 相关依赖
- Python3.7+
- pipenv
- nmap

### 安装依赖服务
```
$ sudo apt install nmap
$ sudo -H pip install pipenv
```

### 初始化虚拟环境
```
$ pipenv install 
```

### 启动虚拟环境
```
$ pipenv shell 
```

### 创建数据库
#### 方法1
```
$ flask shell
>>> from pam import db
>>> db.create_all()
```
#### 方法2
```
$ flask initdb
```
### 运行程序
```
$ flask run 
```

访问`127.0.0.1:5000/project`



