เราจะลอง Deploy Web Application แบบ manual Step by Step ดูครับ

Step 0: ทำการสร้าง VM ด้วย vagrant กันก่อน (base on Centos7)
```
vagrant up

vagrant ssh webapp
```
Step 1: ติดตั้ง package ที่ต้องใช้งาน
```
sudo yum install -y epel-release 
sudo yum install -y python python-pip wget

sudo pip install flask flask-mysql
```
Step 2: ติดตั้ง mysql และ configure
```
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm

sudo rpm -ivh mysql-community-release-el7-5.noarch.rpm

sudo yum update

sudo yum -y install mysql-server

sudo service mysql start
```
Step 3: ทำการสร้าง database และ user database
```
[vagrant@webapp ~]$ sudo mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.6.50 MySQL Community Server (GPL)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE DATABASE employee_db;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL ON *.* to db_user@'localhost' IDENTIFIED BY 'Passw0rd';
Query OK, 0 rows affected (0.00 sec)

mysql> USE employee_db;
Database changed
mysql> CREATE TABLE employees (name VARCHAR(20));
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO employees VALUES ('JOHN');
Query OK, 1 row affected (0.00 sec)

mysql> quit
Bye
[vagrant@webapp ~]$
```
Step 4: ทำการ Copy app.py และทำการ run 

```
[vagrant@webapp ~]$ cat > app.py
import os
from flask import Flask
from flaskext.mysql import MySQL      # For newer versions of flask-mysql
# from flask.ext.mysql import MySQL   # For older versions of flask-mysql
app = Flask(__name__)

mysql = MySQL()

mysql_database_host = 'MYSQL_DATABASE_HOST' in os.environ and os.environ['MYSQL_DATABASE_HOST'] or  'localhost'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'db_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Passw0rd'
app.config['MYSQL_DATABASE_DB'] = 'employee_db'
app.config['MYSQL_DATABASE_HOST'] = mysql_database_host
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
    return "Welcome!"

@app.route('/how are you')
def hello():
    return 'I am good, how about you?'

@app.route('/read from database')
def read():
    cursor.execute("SELECT * FROM employees")
    row = cursor.fetchone()
    result = []
    while row is not None:
      result.append(row[0])
      row = cursor.fetchone()

    return ",".join(result)

if __name__ == "__main__":
    app.run()
^C
[vagrant@webapp ~]$ 
```

ทำการ Run Web Server
```
export FLASK_ENV=development
FLASK_APP=app.py flask run --host=0.0.0.0
```

ลองทดสอบเรียก ไปที่ 
```
http://<IP>:5000                                                    => Welcome
http://<IP>:5000/how%20are%20you                   => I am good, how about you?
http://<IP>:5000/read%20from%20database     => JOHN
```