# เรื่อง Templating Jinja2

การกำหนด configuration ในการ deploy ระบบต่างๆ นั้น ก่อนหน้านี้เราทำการกำหนดค่า configuration ต่างๆ เป็นแบบ static หรือการกำหนดเข้าไปตรงๆ เลย ตามแต่ละระบบ ทีนี้ ถ้าเกิดว่าเราต้องทำการเขียนเป็นลักษณะของ template configuration ให้สามารถนำไปใช้ได้กับหลายๆ การ deploy ระบบที่แตกต่างกันเช่น ในเรื่องของ user,password, ip address หรือ version ต่างๆ จะทำอย่างไร? และในปัจจุบันมีการใช้งานระบบ Cloud ในการ deploy app มากขึ้น การกำหนดค่าที่เป็น static คงไม่เหมาะสมนัก

ดังนั้น การกำหนดค่า static ต่างๆ ให้เป็นในรูปแบบของ ตัวแปรบน configuration แทน นั้นคือ การใช้รูปแบบ template เช่น

```
My name is Supachai Jaturaprom
```
ใช้เป็นตัวแปร แทน
```
My name is {{ my_name }}
```

ใน ansible playbook ก็จะเป็นแบบนี้
```
-
    name: Test Template Playbook
    hosts: localhost
    vars:
        my_name: Supachai Jaturaprom
    tasks:
        - debug: 
            msg: "My name is {{ my_name }}"
```

## Jinja2 Template

Jinja คือ ภาษาที่ถูกใช้ในการสร้าง Template ที่ช่วยให้เราสร้าง configuration แบบ dynamic ได้ เพื่อนำไปใช้ได้อย่างยืดหยุ่น ข้อมูลเพิ่มเติม https://jinja.palletsprojects.com/en/2.10.x/

### เรื่อง String Manipulation - Filter

- Substitute
- Upper
- Lower
- Title
- Replace
- Default

ตัวอย่าง
```
The name is {{ my_name }} -------> The name is Bond
The name is {{ my_name | upper }} -------> The name is BOND
The name is {{ my_name | lower }} -------> The name is bond
The name is {{ my_name | title }} -------> The name is Bond 
The name is {{ my_name | replace ("Bond","Bourne")}} -------> The name is Bourne
The name is {{ first_name | default ("James")}} {{ my_name }} --> The name is James Bond
```

### เรื่อง Filters - List and Set

- min
- Upper
- unique
- union
- interest
- random

ตัวอย่าง
```
{{ [ 1, 2, 3 ] | min }}                       => 1
{{ [ 1, 2, 3 ] | max }}                       => 3
{{ [ 1, 2, 3, 2 ] | unique }}                 => 1, 2, 3
{{ [ 1, 2, 3, 4] | union ([ 4, 5 ]) }}        => 1, 2, 3, 4, 5
{{ [ 1, 2, 3, 2 ] | intersect  ([ 4, 5 ])}}   => 4
{{ 100 | random }}                            => Random number
{{ ["The", "name", "is", "Bond"]} | join ("")}} => The name is Bond
```

### เรื่อง Filters - File


```
{{ "/etc/hosts" | basename }}                       => hosts
{{ "c:\windows\hosts" | win_basename }}             => hosts
{{ "c:\windows\hosts" | win_splitdrive }}           => ["c:","\windows\hosts"]
{{ "c:\windows\hosts" | win_splitdrive | first }}   => "c:"
{{ "c:\windows\hosts" | win_splitdrive | last }}    => "\windows\hosts"
```

เอกสารเพิ่มเติม 
- https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-builtin-filters
- https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#filters-for-formatting-data

### Template Jinja2 Execise 

Exec 1:  Update the msg field in debug task to print - "The name is bond! james bond!" 
```
-
  name: Test Jinja2 Templating
  hosts: localhost
  vars:
    first_name: james
    last_name: bond
  tasks:
  - debug:
      msg: 'The name is {{ last_name }}! {{ first_name }} {{ last_name }}!'
```

Exec 2: Update the msg field in debug task to print name in title case - "The name is bond! james bond!"

```
-
  name: Test Jinja2 Templating
  hosts: localhost
  vars:
    first_name: james
    last_name: bond
  tasks:
  - debug:
      msg: 'The name is {{ last_name | title }}! {{ first_name | title }} {{ last_name | title }}!'

```

Exec 3: Update the msg field in debug task to print the lowest number inthe given list using janja2 filter "min" - "Lowest = 6"
```
-
  name: Test Jinja2 Templating
  hosts: localhost
  vars:
    array_of_numbers:
      - 12
      - 34
      - 06
      - 34
  tasks:
  - debug:
      msg: 'Lowest = {{ array_of_numbers | min }}'
```

Exec 4: We are given two lists of dependent packages to install. A playbook has been written with a task to install dependencies.

Task: Identify the unique packages from the two lists (<b>web_dependencies</b> and <b>sql_dependencies</b>) using jinja2 filter union and apply it in the given space under <b>with_items</b>.
```
-
  name: Install Dependencies
  hosts: localhost
  vars:
    web_dependencies:
         - python
         - python-setuptools
         - python-dev
         - build-essential
         - python-pip
         - python-mysqldb
    sql_dependencies:
         - python
         - python-mysqldb
  tasks:
  - name: Install dependencies
    apt: name='{{ item }}' state=installed
    with_items: '{{ web_dependencies | union (sql_dependencies) }}'
```

Exce 5: We are trying to write a playbook to generate a file with random name everytime. The first name must be /tmp/random_file_ followed by a random number. eg: /tmp/random_file_1234

<b>Task:</b> Update the task to modify the file name to use a random number suffix anywhere from 0 to 1000.

```
-
  name: Generate random file name
  hosts: localhost
  tasks:
  - name: Install dependencies
    file:
      path: /tmp/random_file_{{ 1000 | random }}
      state: touch
```

Exec 6: Test if a given variable has a valid IP address.

<b>Task:</b> Apply the <b>ipaddr</b> filter to the <b>ip_address</b> in the msg field of debug task to test if IP is valid. it will return false if IP is invalid

```
-
  name: Test valid IP Address
  hosts: localhost
  vars:
    ip_address: 192.168.1.6
  tasks:
  - name: Test IP Address
    debug:
      msg: IP Address = {{ ip_address | ipaddr }}
```

Exec 7: Retrieve the file name from a given path in linux.

<b>Task:</b> Use the '<b>basename</b>' filter to retrieve the file name.

```
-
  name: Get filename
  hosts: localhost
  vars:
    file_path: /etc/hosts
  tasks:
  - name: Get filename
    debug:
      msg: File Name = {{ file_path | basename }}
```