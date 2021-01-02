# เรื่อง Ansible Role

ทำไม ต้องใช้ Role
- Organize
- Re-Use
- Share

## Organize 

```
ansible-galaxy init webserver
```

ภายใต้โฟเดอร์​ webserver

    - README.md
    - tests
    - tasks
    - handlers
    - vars
    - defaults
    - meta

### Re-Use

```
- 
    name: Deploy
    hosts: web
    roles:
        - webserver
```

### Share

```
ansible-galaxy import webserver
```

### Include to Roles

ตัวอย่าง Ansible Playbook
```
-
    name: Deploy Web Application
    hosts: db_and_web_server
    tasks:
        - include: tasks/deploy_db.yml
        - include: tasks/deploy_web.yml
```

ตัวอย่าง Ansible Tasks File tasks/deploy_db.yml
```
    - name: Install dependencies
    - name: Install MySQL database
    - name: Start Mysql Service
    - name: Create Application Database
    - name: Create Application DB User
```

ตัวอย่าง Ansible Tasks File tasks/deploy_web.yml
```
    - name: Install Python Flask dependencies
    - name: Copy web-server code
    - name: Run Web-Server
```

ทำการสร้าง role โดยอ้างอิงจาก tasks ข้างต้น
```
ansible-galaxy init mysql_db
ansible-galaxy init flask_web
```
จากนั้นเราจะอ้างอิงในไฟล์​ playbook แบบนี้
```
-
    name: Deploy Web Application
    hosts: db_and_web_server
    roles:
        - mysql_db
        - flask_web
```

## Distribute application model

เราสามารถ deploy แบบ single หรือ multinode ได้ ตัวอย่างเช่น

All-in-one node
```
-
    name: Deploy Web Application
    hosts: db_and_web_server
    roles:
        - mysql_db
        - flask_web
```

Mutli nodes
```
-
    name: Deploy Database
    hosts: db_server
    roles:
        - mysql_db

-
    name: Deploy Web Application
    hosts: web_server
    roles:
        - flask_web
```

## Ansible Roles Demo

เข้าไปที่ simple_webapp_v3 ทำการสร้างโฟเดอร์​ชื่อ roles
จากนั้นใช้คำสั่ง
```
cd roles
ansible-galaxy init mysql_db

```
ทำการสร้างโฟเดอร์​ flask_web และ python พร้อมกับสร้างโฟเดอร์​ tasks กับไฟล์​ main.yml

จากนั้นย้าย tasks ต่างๆ เข้าไปภายใต้ไฟล์​ main.yml ของแต่ละ roles 

ทำการเปลี่ยนจาก tasks: เป็น roles: แทน และใส่ชื่อ roles ที่เราสร้างไว้ก่อนหน้านี้ แบบ list ตามลำดับการทำงาน
```
-
  name: Deploy a web application
  hosts: all
  become: yes
  become_method: sudo
  roles:
    - python
    - mysql_db
    - flask_web
```

### Ansible Galaxy - Public Roles
ภายใต้โฟเดอร์​ roles/mysql_db ซึ่งเราใช้คำสั่ง ansible-galaxy init แล้ว จากนั้นทำการแก้ไข ไฟล์ต่างๆ
- ./README.md --------> เขียนอธิบายการใช้งาน ansible role 
- ./mysql_db/meta/main.yml -----> เขียนคุณสมบัติเกี่ยวกับ ansible role

จากนั้น ก็ทำการสร้าง repo บน github แล้วทำการ initial git ดังนี้
```
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/supachai-j/ansible-role-mysql.git
git push -u origin main
```
หลังจาก upload ไฟล์​ ทั้งหมดขึ้นไปแล้ว 
- จากนั้นทำการ Login ที่ https://galaxy.ansible.com/
- แล้วทำการ เลือก github account sign-in 
- เลือก My Content และเลือก + add Content 
- แล้วเลือก repo ที่เราต้องการ upload ขึ้นไป 
แค่นี้ก็เรียบร้อย

ตัวอย่างที่ upload ขึ้นไป

https://galaxy.ansible.com/supachai_j/ansible_role_mysql

ในการใช้งานเราสามารถ search roles จาก ansible galaxy ได้
```
ansible-galaxy search mysql
```