# 环境安装

## 软件环境说明
- python版本:3.7以上
- django版本:2.1.7
- 推荐使用虚拟环境virtualenv,(安装命令:pip install virtualenv)
- virtualenv venv --python=python3 (生成虚拟环境)
- ./venv/bin/pip install -r requirements.txt

# nio-ops-framework
nio-ops-framework base on cmdb

# 创建管理员
python manage.py createsuperuser


# 启动workflow

## 同步workflow数据库
- python3 manage.py makemigrations --settings workflow.settings
- python3 manage.py migrate --run-syncdb --settings workflow.settings

## 启动workflow服务
./manage.py runserver --settings workflow.settings

# 启动cmdb

## 同步cmdb数据库
- python3 manage.py makemigrations --settings cmdb.settings
- python3 manage.py migrate --run-syncdb --settings cmdb.settings

## 启动cmdb服务
./manage.py runserver --settings cmdb.settings