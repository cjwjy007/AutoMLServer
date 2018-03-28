运行思路

运行任务时，运行taskcontroller中的run_task, 初始化一个task对象，这个对象会将json文件转换为结点与边的数据结构，
并将json中的config添加到结点对象中。之后取出入度为0的结点，创建新线程运行，运行结束的回调会更新该节点后继结点的入度，
直到所有结点运行完毕。


前端添加新结点

1.在src/components/MLMain/MLComponents/CompModel.js中添加json

2.在src/components/MLMain/MLComponents/Config中添加结点配置的xx.vue文件

3.在src/components/MLMain/MLComponents/ConfigTable.js中引入xx.vue文件

4.修改Project.vue中的动态路由表，在components中添加”xx”: ConfigTable[“xx”]


后端添加新结点

1.在automl/mltask/tasknode中添加结点类继承BaseNode，具体参考其他结点实现。

2.在automl/mltask/nodefactory中注册结点


前端部署（在项目路径中）

1.修改src/baseurl.js至后端IP地址:端口

2.运行npm run build 编译项目

3.sudo mv dist ‘path under server’移动到服务器路径


后端部署(比较复杂，有可能会出问题)

1.安装anaconda

2.安装redis 并启动服务

sudo apt-get install redis-server

service redis start

（在项目路径中）

1.修改config中数据库密码，root@your password ，启动mysql数据库

2.pip install -r requirement.txt 安装依赖

3.conda install -c conda-forge xgboost 安装xgboost

4.conda install -c conda-forge celery 安装celery

5.python initdb.py 导入数据库表

6.nohup celery -A automl.celery worker -P eventlet -c 100 & 启动celery的后台运行worker

7.nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:9977 automl:app > ../automl_log.out 2>&1 & 启动服务器