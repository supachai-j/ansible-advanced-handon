# เรื่อง Asynchronous Actions

Ansible -----ssh------> Target
- Run a process and chcek on it later
- Run multiple processes at once and check on them later
- Run processes and forget

## ASYNC & POLL

Example ansible playbook
```
-
    name: Deploy Web Application
    hosts: db_and_web_server
    tasks:
        -
            command: /opt/monitor_webapp.py
            async: 360
            poll: 60

```
- คำสั่ง async คือ How long to run ?
- คำสั่ง poll คือ How frequently to check? (by default 10 seconds)
- ถ้ากำหนด poll เท่ากับ 0 หมายถึง จะไม่ทำการ รอผลของ task นั้น จะทำ task ต่อไปเลย

```
-
    name: Deploy Web Application
    hosts: db_and_web_server
    tasks:
        -
            command: /opt/monitor_webapp.py
            async: 360
            poll: 0
            register: webapp_result
        -
            command: /opt/monitor_database.py
            async: 360
            poll: 0
            register: database_result
        -
            name: Check status of tasks
            async_status: jid={{ webapp_result.ansible_job_id }}
            register: job_result
            until: job_result.finished
            retries: 30

```

async_status คือ การตรวจสอบสถานะของงาน (tasks) ที่เป็นแบบ async

## Asynchronous action Practices Testing

### โจทย์​ข้อ 1
ต้องการให้เพิ่ม play ใหม่ตอนท้ายของไฟล์​ playbook ที่ใช้ในการ monitor ตัว web application สำหรับ 6 นาที เพื่อมั่นใจว่า web application ทำงานปกติ
แต่เราไม่ต้องการให้เปิด SSH Connection ค้างไว้ในระหว่างทำการ execution คำสั่ง

```
-
  name: Deploy a mysql DB
  hosts: db_server
  roles:
    - python
    - mysql_db


-
  name: Deploy a Web Server
  hosts: web_server
  roles:
    - python
    - flask_web

-
  name: Monitor Web Application for 6 Minutes
  hosts: web_server
  command: /opt/monitor_webapp.py
  async: 360

```
### โจทย์​ข้อ 2
โดยปกติค่าเริ่มต้นของ polling จะเท่ากับ 10 วินาที เราต้องการให้เพิ่มเป็นการ polling ทุกๆ 30 วินาที
```
-
  name: Deploy a mysql DB
  hosts: db_server
  roles:
    - python
    - mysql_db

-
  name: Deploy a Web Server
  hosts: web_server
  roles:
    - python
    - flask_web

-
  name: Monitor Web Application for 6 Minutes
  hosts: web_server
  command: /opt/monitor_webapp.py
  async: 360
  poll: 30

```
### โจทย์​ข้อ 3
เราต้องการเพิ่ม monitoring ใหม่สำหรับ database เท่ากับ 6 นาที แต่ต้องทำการเป็นลักษณะ parallel ที่ไม่ต้องรอกันกับ monitor ตัวอื่นๆ เช่น web application 
```
-
  name: Deploy a mysql DB
  hosts: db_server
  roles:
    - python
    - mysql_db

-
  name: Deploy a Web Server
  hosts: web_server
  roles:
    - python
    - flask_web

-
  name: Monitor Web Application for 6 Minutes
  hosts: web_server
  command: /opt/monitor_webapp.py
  async: 360
  poll: 0

-
  name: Monitor Database for 6 Minutes
  hosts: db_server
  command: /opt/monitor_database.py
  async: 360
  poll: 0

```
### โจทย์​ข้อ 4
เราไม่ต้องการแบบ "fire and forget" โดยเราต้องการตรวจสอบทีหลัง โดยให้ผลลัพธ์​ สามารถอ้างอิงในตัวแปร webapp_result และ database_result ได้
```
-
  name: Deploy a mysql DB
  hosts: db_server
  roles:
    - python
    - mysql_db

-
  name: Deploy a Web Server
  hosts: web_server
  roles:
    - python
    - flask_web

-
  name: Monitor Web Application for 6 Minutes
  hosts: web_server
  command: /opt/monitor_webapp.py
  async: 360
  poll: 0
  register: webapp_result

-
  name: Monitor Database for 6 Minutes
  hosts: db_server
  command: /opt/monitor_database.py
  async: 360
  poll: 0
  register: database_result

```