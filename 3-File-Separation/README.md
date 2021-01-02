# เรื่อง File Separation

## Variable of Inventory
ตัวอย่าง Inventory File Inventory
```
db_and_web_server ansible_ssh_pass=Passw0rd ansible_host=192.168.1.14
```
โดยเราจะทำการย้าย ค่าตัวแปรต่างๆ ไปไว้ไฟล์​ yml ภายใต้ โฟเดอร์​ host_vars และชื่อไฟล์​ ตัวเหมือนกันกับชื่อ target ดังนี้
playbook.yml
host_vars
    - db_and_web_server.yml

Inventory File Inventory
```
db_and_web_server
```
Simple Variable File - host_vars/db_and_web_server.yml
```
ansible_ssh_pass: Passw0rd
ansible_host: 192.168.1.14
```

นอกจากในการกำหนด variable ของแต่ละ host ด้วยไฟล์​ yml ภายใต้โฟเดอร์​ host_vars แล้ว
ยังสามารถกำหนดตัวแปร variable ให้กับแต่ละกลุ่มได้โดย กำหนดภายใต้โฟเดอร์​ group_vars ได้เช่นกัน

## Include of Tasks

ปกติเราจะทำการเขียน Tasks ต่างๆ ไว้บนไฟล์​ playbook ไฟล์เดียว ดังนี้
Ansible Playbook
```
- 
    name: Deploy web Application
    hosts: db_and_web_server
    tasks:
        - name: Install dependencies

        - name: Install MySQL database

        - name: Start MySQL Service

        - name: Create Application Databases

        - name: Create Application DB User

        - name: Install Python Flask dependencies

        - name: Copy web-server code

        - name: Run Web-Server
```

แต่โดยเราสามารถแยก Tasks ต่างๆ บนไฟล์​ yml ไว้ภายใต้โฟเดอร์ tasks แล้วใช้คำสั่ง include ดังนี้

Ansible Playbook
```
- 
    name: Deploy Web Application
    hosts: db_and_web_server
    tasks:
        - include: tasks/deploy_db.yml

        - include: tasks/deploy_web.yml
```

Ansible Tasks File tasks/deploy_db.yml
```
      - name: Install dependencies

        - name: Install MySQL database

        - name: Start MySQL Service

        - name: Create Application Databases

        - name: Create Application DB User
```

Ansible Tasks File tasks/deploy_web.yml
```
        - name: Install Python Flask dependencies

        - name: Copy web-server code

        - name: Run Web-Server
```