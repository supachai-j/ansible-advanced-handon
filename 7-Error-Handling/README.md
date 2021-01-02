# เรื่อง Error Handling

## Task Failure
ตัวอย่างของ ansible playbook
```
-
    name: Deploy Web Applications
    hosts: server1, server2, server3
    tasks:
        - name: Install dependencies
            ----- code hidden -----
        - name: Install MySQL database
            ----- code hidden -----
        - name: Start Mysql Service   <--------------------- Failure 
            ----- code hidden ----
        - name: Install Python Flask dependencise
            ----- code hidden -----
        - name: Run web-server
            ----- code hidden -----
```
จากตัวอย่าง task ข้างต้น ถ้าเกิด task failure ที่ตอน start mysql service ในการ deploy แบบ single node จะออกจาก deploy เลย

แต่สำหรับการ deploy แบบ multi nodes ถ้าเกิด task failure ที่ server2 แต่ target อื่นๆ ไม่มี task failture ก็จะ skip server2 ไป แล้วทำ task อื่นๆ ต่อไปใน server1 และ server3 จนเสร็จ

## Any Error Fatal
เป็นการกำหนดให้มีเงื่อนไขว่า ถ้าเกิด task failure ที่ target ตัวใดๆ ให้หยุดทำงานต่อ
```
-
    name: Deploy Web Applications
    hosts: server1, server2, server3
    any_errors_fatal: true
    tasks:
    -------- hidden contents -----------
```
งั้นสถานการณ์ที่เกิดปัญหาเหมือนก่อนหน้านี้ ที่เกิด task failure ที่ server2 ในกระบวนการ start mysql service แล้วนั้น จะทำให้ ansible หยุดการทำงานต่อทั้งหมด

## Ignore Errors, Failed_When

ตัวอย่างเช่น 
```
-
    name: Deploy Web Applications
    hosts: server1, server2, server3
    any_errors_fatal: true
    tasks:
    -------- hidden contents -----------
        - mail: 
                to: devops@company.com
                subject: Server Deployed!
                body: Web Server Deployed
          ignore_errors: yes
        
        - command: cat /var/log/server.log
           register: command_output
           failed_when: "'ERROR' in command_output.stdout"
```
- ignore_errors คือ การไม่สนใจ error ที่เกิดขึ้นของ task และทำงานต่อไป
- failed_when คือ การกำหนดเงื่อนไขในการ Failure ของ task

ตัวอย่าง การ deploy application โดยใช้ any_errors_fatal และ ignore_errors
```
-
  name: Deploy a web application
  hosts: app_servers
  any_errors_fatal: true
  vars:
    db_name: employee_db
    db_user: db_user
    db_password: Passw0rd
  tasks:
    - name: Install dependencies
      apt: name={{ item }} state=installed
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
        state:  installed
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

    - name: "Send notification email"
      mail:
        to: devops@corp.com
        subject: Server Deployed!
        body: Web Server Deployed Successfully
      ignore_errors: yes
```