# เรื่อง Ansible Vault

อะไรคือ Ansible Vault ?

ยกตัวอย่างไฟล์ Inventory ก่อนหน้านี้ที่เราใช้ในการสั่งงาน ansible ให้อ้างอิง target ว่ามีค่าตัวแปรที่กำหนดอะไรบ้าง 
```
# Inventory File - Inventory.txt

db_server ansible_host=192.168.1.1 ansible_ssh_pass=Passw0rd <--รหัสแบบ Cleartext
web_server ansible_host=192.168.1.2 ansible_ssh_pass=Passw0rd <--รหัสแบบ Cleartext

```
จากไฟล์ด้านบน ก็จะเห็น password หรือรหัสผ่าน ที่ใช้เข้า ssh ไปยัง target ทั้งสองตัว เป็นแบบ Cleartext ก็เลยทีเดียว งั้นในแง่ความปลอดภัย ก็ต้องบอกว่า ใครได้ไฟล์​ inventory.txt ก็จบแน่นวล 

งั้นต้องมีวิธีการอะไรสักอย่างมาช่วยในการป้องกัน ข้อมูลที่เป็น Credentials ต่างๆ สำหรับ <b>Ansible Vault</b> จะเข้ามาแก้ไขในเรื่องนี้ โดย ansible vault จะทำการเข้ารหัสลับ (Encryption) ไฟล์​ Inventory.txt ให้โดยใช้คำสั่ง
```
ansible-host$ cat inventory.txt
target10 ansible_host=192.168.55.30 ansible_user=root ansible_ssh_pass=vagrant
ansible-host$
ansible-host$ ansible-vault encrypt inventory.txt
New Vault password:                                 <------ ใส่รหัส
Confirm New Vault password:                         <------ ใส่รหัสอีกครั้ง
Encryption successful
ansible-host$
ansible-host$ cat inventory.txt
$ANSIBLE_VAULT;1.1;AES256
33323964346638373364363064366237393235316431666664666132353633303564663666656532
6438663935366531376339316330666666393734373631330a336538623032356366313037313162
38363330303331326566313031376231356263643137323365346564626637663961353732646338
3035643337626233340a663766303061376531336530636663336234306538633133666366633861
35303463643537636435653334613337336662663834643239313939303535663930653737393830
63663233303565633332386434396131633832646231386334653531653932653265343963393134
38663665353539616135343636623165653963623130376538623030326433346138396265333361
31366162386334646337
```
ดังนั้นตอนที่ใช้คำสั่ง ansible หรือ ansible-playbook ต้องเพิ่ม --ask-vault-pass ด้วย
```
ansible-host$ ansible all -m ping -i inventory.txt --ask-vault-pass
Vault password:               <-------- ใส่รหัสที่เหมือนกันกับข้างต้น
target10 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

ในการอ้างอิง รหัสผ่านในการ Decrpytion ในการใช้คำสั่ง ansible ต่างๆ ที่ใช้ inventory.txt ไฟล์ นั้น สามารถใช้วิธีอ้างอิงได้ดังนี้
1. อ้างอิงด้วยไฟล์ รหัสผ่าน 
```
ansible-playbook playbook.yml -i inventory.txt --vault-password-file=~./valut_pass.txt
```
2. อ้างอิงด้วยไฟล์ scripts
```
ansible-playbook playbook.yml -i inventory.txt --vault-password-file=~./valut_pass.py
```
โดยที่เราสามารถใช้ scripts เรียกไปที่ระบบที่เก็บรหัสผ่าน ที่มีความปลอดภัยอีกระบบหนึ่งก็ได้

คำสั่งที่ใช้ดูไฟล์​ inventory ที่ถูกเข้ารหัสลับ
```
ansible-vault view inventory.txt 
```
คำสั่งสร้างไฟล์​ inventory ใหม่ ที่ถูกเข้ารหัสลับ 
```
ansible-vault create inventory2.txt
```