# เรื่อง Custom Modules

ในการทำงานต่างๆ Ansible จะอาศัยความสามารถต่างๆ ที่ได้ จากสิ่งที่เรียกว่า module พระเอกที่ชื่อว่า module ถูกพัฒนาขึ้นมาจากหลายๆ กลุ่มบุคคล ไม่ว่าจะเป็นทางผู้พัฒนา ansible เองหรือจะเป็นจากทางผู้พัฒนา Vendor/Product นั้นๆ เพื่อให้ สามารถใช้ ansible กับอุปกรณ์หรือโปรแกรมของเขาได้

ตัวอย่าง เช่น
```
#Simple Ansible Playbook1.yml
-
    name: Set Firewlal Configurations
    hosts: web
    tasks:
        - firewalld:
            service: https
            permanent: true
            state: enabled
        - service:
            name: mysql
            state: started
        
        - command: cat /etc/hosts
        - debug: msg='This is test message'
```

ตัวอย่าง Module ที่เราใช้กัน
- System
- commands
- File
- Database
- Cloud
- Windows
- More....

## Custom Debug module
การใช้งาน debug module ปกติ
```
-
    name: Debug somting
    hosts: target1
    tasks:
        - debug: msg='This is test message'
```
Output
```
TASK [debug]*********************************************************************
ok: [target1] => {
    "msg": " This is test message"
}
```
การใช้งาน custom debug module
```
-
    name: Debug somting
    hosts: target1
    tasks:
        - custom_debug: msg='This is test message'
```
Output
```
TASK [debug]*********************************************************************
ok: [target1] => {
    "msg": " Sat 29 Jul 17:33:33 BST 2017 - This is test message"
}
```

## ตัวอย่าง Module Coding

```
#! /usr/bin/python

# Import JSON
try:
    import json
except ImportError:
    import simplejson as json

# Import AnsibleModule
from ansible.module_utils.basic import AnsibleModule
import time
import sys

# Instantiate AnsibleModule
def main():
        module = AnsibleModule(
            argument_spec = dict (
                msg=dict(required=True, type='str')
            )
        )

        msg = module.params['msg']

        # Successfull Exit
        try: 
            module.exit_json(changed=True, msg='%s - %s' % (time.strftime("%c"), msg))
        except:
        Fail Exit
            module.fail_json(msg="Error Message")
if __name__ == '__main__':
    main()
```

## Best Practice - Documentation

```
ansible-doc debug
```

```
#!/usr/bin/python

DOCUMENTATION = '''
---
module: custom_debug
short_description: A custom debug module
..........
.....
...

'''

EXAMPLES = '''
# Example 
custom_debug: 
    msg: This is test message

'''
```

## แล้ว Ansible Module ถูกเก็บไว้ที่ไหน

- All buil-in modules are located by default under
- Role - place it under library folder inside project
- Across project - place anywhere and input using env variable ANSIBLE_LIBRARY

http://github.com/ansible/ansible/tree/devel/lib/ansible/modules


## Ansible Playable Project 
https://gitlab.com/jandradap/ansible-playable
