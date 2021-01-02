# เรื่อง Ansible Dynamic Inventory
ในการกำหนดไฟล์ inventory ปกติเราจะทำการกำหนดแบบ static ไว้ ไม่ว่าจะเป็นค่าต่างๆ ของ target หรือการอ้างอิงตัวแปรด้วยไฟล์​ variable ต่างๆ ก็เช่นกัน
```
# Inventory File - inventory.txt
db_server ansible_host=192.168.1.1
web_server ansible_host=192.168.1.2
```
ปัญหามีอยู่ว่า ถ้า target ต่างๆ ที่กำหนด ไม่สามารถกำหนดแบบ static ได้ล่ะ เช่น เครื่องที่อยู่บนระบบ cloud หรือระบบที่ต้องมีการเปลี่ยนแปลงอยู่ตลอดจะทำอย่างไร ?

ดังนั้น ในการกำหนด Inventory แบบ Dynamic จึงเป็นคำตอบ

Ansible -------> CMDB or any other Cloud API

ตัวอย่าง python script สำหรับเชื่อมต่อไปยัง CMDB หรือ API อื่นๆ 
```
#! /usr/bin/env python

import json

# Get inventory data from source - CMDB or any other API
def get_inventory_data():
    return {
        "databases": {
            "hosts":["db_server"]
            "vars": {
                "ansible_ssh_pass":"Passw0rd",
                "ansible_ssh_host": "192.168.1.1"
            }
        },
        "web": {
            "hosts":["web_server"]
            "vars": {
                "ansible_ssh_pass":"Passw0rd",
                "ansible_ssh_host": "192.168.1.2"
            }
        }
    }
# Default main function
if __name__ == "__main__":
    inventory_data = get_inventory_data()
    print(json.dumps(inventory_data))
```

ในการเรียกใช้ก็เหมือนกัน
```
ansible-playbook playbook.yml -i inventory.txt

ansible-playbook playbook.yml -i inventory.py
```

### Inventory Scripts

```
./inventory.py --list
```

```
./inventory.py --host web
```