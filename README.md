# PAM
PockrAssetManagement 破壳资产管理工具
![](https://other-1256870184.cos.ap-beijing.myqcloud.com/2019-09-26-127.0.0.1_5000_project.png)
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
```
$ flask shell
>>> from pam import db
>>> db.create_all()
```

### 运行程序
```
$ flask run 
```

访问`127.0.0.1:5000`



