# Deploy Web App with Ansible

ให้เข้าไปดูที่โฟเดอร์​ simple_web_app_ansible
จะมีไฟล์​ [inventory.txt](vagrant-webapp-ansible/inventory.txt) ที่เก็บ target hosts อยู่
มีไฟล์​ [app.py](vagrant-webapp-ansible/app.py) เป็น python wep app ที่สามารถ run บน Flask Web Application ได้

จากนั้นให้ทำการสร้าง VMs โดยใช้คำสั่ง 
โดยเข้าไปที่โฟเดอร์ vagrant-webapp-ansible
```
vagrant status

vagrant up
```

ในการสร้าง VMs จะมีการ deploy ansible ในแต่ละ VMs เรียบร้อยเลย ด้วยไฟล์​ [playbook.yml](vagrant-webapp-ansible/playbook.yml)

เมื่อเสร็จแล้วก็สามารถทดสอบ โดยเรียกไปที่ 
```
http://192.168.55.26:5000    <---------------- Welcome!
http://192.168.55.27:5000   <---------------- Welcome!

http://192.168.55.26:5000/how%20are%20you    <---------------- I am good, how about you?
http://192.168.55.27:5000/how%20are%20you    <---------------- I am good, how about you?

http://192.168.55.26:5000/read%20from%20database    <----------------JOHN
http://192.168.55.27:5000/read%20from%20database    <----------------JOHN
```
### Coding Exercise
```
-
  name: Deploy a web application
  hosts: db_and_web_server
  vars:
    db_name: "employee_db"
    db_user: "db_user"
    db_password: "Passw0rd"
  tasks:
    - name: Install dependencies
      apt: name={{ item }} state=present
      with_items:
       - python
       - python-setuptools
       - python-dev
       - build-essential
       - python-pip
       - python-mysqldb

    - name: Install MySQL database
      apt:
        name: "{{ item }}"
        state:  present
      with_items:
       - mysql-server
       - mysql-client

    - name: Start Mysql Service
      service:
        name: mysql
        state: started
        enabled: yes

    - name: Create Application Database
      mysql_db: name={{ db_name }} state=present


    - name: Create Application DB User
      mysql_user: name={{ db_user }} password={{ db_password }} priv='*.*:ALL' host='%' state='present'

    - name: Install Python Flask dependencies
      pip:
        name: '{{ item }}'
        state: present
      with_items:
       - flask
       - flask-mysql

    - name: Copy web-server code
      copy: src=app.py dest=/opt/app.py

    - name: Start web-application
      shell: FLASK_APP=/opt/app.py nohup flask run --host=0.0.0.0 &
```