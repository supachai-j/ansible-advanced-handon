# เรื่อง File Lookup

ถ้าเรามีไฟล์ CSV ที่เป็น credential.csv 
```
Hostname,Password
Targe1, Passw0rd
Targe2, Passw0rd
```

```
{{ lookup('csvfile','target1 file=/tmp/credentials.csv delimiter=,')}} =>Passw0rd
```
- csvfile คือ ชนิดของไฟล์
- target1 คือ ค่าหรือตัวแปรที่เราต้องการค้นหา (lookup)
- file=/.../....csv คือ อ้างอิงไฟล์ที่เราต้องการค้นหา

จากการค้นหาข้างต้น จะได้ผลลัพธ์​คือ Passw0rd ออกมา

ในการใช้งาน File Lookup ยังรองรับชนิดไฟล์​
- INI
- DNS
- MongoDB

ข้อมูลเพิ่มเติม https://docs.ansible.com/ansible/latest/plugins/lookup.html

## File Lookup Execise
Exec 1: We have moved the credentials for hosts out of the inventory file and into a separate csv file called credentials.csv. Check it out! In the given playbook, the password for the host web_server is hard-coded into a vaiable <b>ansible_ssh_pass</b>.

<b>Task:</b> Replace the Ansible Password field to use "lookup" plugin to lookup a "csvfile", the file is "credentials.csv" and the value to lookup is "web_server".
```
-
  name: Test Connectivity
  hosts: web_server
  vars:
    ansible_ssh_pass: "{{ lookup('csvfile','web_server file=credentials.csv delimiter=,') }}"
  tasks:
  - name: Ping target host
    ping:
           data: "Test"
```
Exec 2: Let us attempt the same operation if the credential file were to be in ini format. In the given playbook, the password for the host web_server is hardcodeed into a vaiable ansible_ssh_pass.

<b>Task:</b> Replace the Ansible Password field to use "lookup" plugin to lookup a "ini" file, the file is "credentials.ini" and the value to lookup is "password" and the section is "web_server".

credentials.ini
```
# Credentials File

[web_server]
password=Passw0rd

[db_server]
password=Passw0rd
```

inventory
```
db_server
web_server
```
playbook.yml
```
-
  name: Test Connectivity
  hosts: web_server
  vars:
    ansible_ssh_pass: "{{lookup('ini','password section=web_server file=credentials.ini') }}"
  tasks:
  - name: Ping target host
    ping:
           data: "Test"
```
