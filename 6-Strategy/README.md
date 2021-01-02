# เรื่องของ Strategy 
## Strategy แบบ LINEAR (เส้นตรง)
ยกตัวอย่างของ ansible ploybook ในการ ติดตั้ง web application ง่ายๆ
```
-
    name: Deploy Web Applications
    hosts: server1
    tasks:
        - name: Install dependencies
            ----- code hidden -----
        - name: Install MySQL database
            ----- code hidden -----
        - name: Start Mysql Service
            ----- code hidden ----
        - name: Install Python Flask dependencise
            ----- code hidden -----
        - name: Run web-server
            ----- code hidden -----
```
ในการทำงาน deploy บน single node
- Dependencies
- Install MySQL
- Start DB
- Install Flask
- Run Server

ทำงานแบบ Step by Step ไปเรื่อยๆ จนจบงาน

อีกตัวอย่างคือ ถ้า deploy บน multi nodes จะเป็นอย่างไร?
```
-
    name: Deploy Web Applications
    hosts: server1, server2, server3
    tasks:
    ---------- hidden contents ----------------
```
ในการทำงานก็จะทำแบบ Step by Step พร้อมกันทั้ง 3 nodes  เรียการทำงานแบบนี้ว่า "Strategy - LINEAR" (เส้นตรง) ซึ่งเป็นพฤติกรรมปกติของ ansible

## Strategy แบบ FREE (อิสระ)

ตัวอย่างของ ansible playbook
```
-
    name: Deploy Web Applications
    strategy: free  <---------------- กำหนด strategy แบบอิสระ
    hosts: server1, server2, server3
    tasks:
        - name: Install dependencies
            ----- code hidden -----
        - name: Install MySQL database
            ----- code hidden -----
        - name: Start Mysql Service
            ----- code hidden ----
        - name: Install Python Flask dependencise
            ----- code hidden -----
        - name: Run web-server
            ----- code hidden -----
```
พอกำหนดแบบนี้ จะทำการ งานที่สั่งไปที่ target แต่ละตัว ทำงานแบบอิสระต่อกัน โดยเครื่องไหนทำงานเสร็จก็ ก็สามารถดำเนินการ tasks ต่อไปได้เลย ไม่ผูกติดว่าต้องทำงานใน task หนึ่งตัวให้เสร็จทั้งหมดก่อน ถึงจะไปอีก task ได้

### Strategy แบบ BATCH 
ตัวอย่างของ ansible playbook
```
-
    name: Deploy Web Applications
    serial: 3  <---- กำหนด serial เท่ากับ 3 และ strategy มีค่าเป็น defualt คือ linear
    hosts: server1, server2, server3, server4, server5
    tasks:
        - name: Install dependencies
            ----- code hidden -----
        - name: Install MySQL database
            ----- code hidden -----
        - name: Start Mysql Service
            ----- code hidden ----
        - name: Install Python Flask dependencise
            ----- code hidden -----
        - name: Run web-server
            ----- code hidden -----
```
ผลที่ได้คือ เป็นการกำหนดการทำงาน deploy ทีละ 3 nodes เสร็จแล้วก็ทำชุดต่อไป และนอกจากจะกำหนดเห็นตัวเลขแล้วยัง กำหนดเป็น percent ได้ (30%) ได้
```
-
    name: Deploy Web Applications
    hosts: server1, server2, server3, server4, server5
    serial: "30%"
```
หรือ กำหนดแบบลักษณะ array ได้ ซึ่งจะทำให้ได้ประโยชน์ในเรื่องการทำ "Rolling Updates" 
```
-
    name: Deploy Web Applications
    hosts: server1, server2, server3, server4, server5
    serial: 
        - 2
        - 3
        - 5
```

### Ansible FORKS
ตัวอย่างของ ansible playbook
```
-
    name: Deploy Web Applications
    hosts: server1, server2... , server100
    tasks:
        - name: Install dependencies
            ----- code hidden -----
        - name: Install MySQL database
            ----- code hidden -----
        - name: Start Mysql Service
            ----- code hidden ----
        - name: Install Python Flask dependencise
            ----- code hidden -----
        - name: Run web-server
            ----- code hidden -----
```
จากตัวอย่างข้างต้น จะสังเกตเห็นว่า มีการกำหนด hosts จำนวน 100 ตัวในการ deploy คำถามคือ ansible จะทำการ deploy พร้อมกันทั้ง 100 ตัว เลยไหม ? คำตอบคือ บ้าบอ (เพลงของ silly fools) ไม่ทำแบบนั้นหรอกครับ แล้วจะทำเท่าไหร่ เราสามารถกำหนดค่านี้จาก forks ในไฟล์ ansible.cfg ครับ
```
forks = 5
```

ข้อมูลเพิ่มเติม
https://docs.ansible.com/ansible/latest/user_guide/playbooks_strategies.html

