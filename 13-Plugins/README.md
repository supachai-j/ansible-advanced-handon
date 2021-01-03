# Ansible Plugins

Ansible จะมี plugins ที่ช่วยให้ทำงานได้ต่างๆ เช่น
- Action
- Connection
- Filter
- Lookup
- Strategy
- Callback

## Custom Filter

- Upper
- Lower
- Title
- replace
- default
- max
- unique
- union
- interest
- random
- join
- basename
- with_basename
- win_splidrive

## Code Custom plugins
```
# Sample Ansible Playbook1.yml
-
    name: Print average marks
    hosts: localhost
    vars:
        marks:
            - 10
            - 20
            - 30
            - 40
    
    tasks:
        - debug:
            msg: ' {{ marks | average }}'
```

/filter_plugins/average.py
```
def verage(list):
        ``` Find average of a list of numbers ```
        return sum(list) / float (len(list))

class FilterModule (object):
        ``` Query filter ```
        def filters (self):
            return {
                'average' : average
            }
```

Run 
```
export ANSIBLE_FILTER_PLUGINS=/filter_plugins;
ansible-playbook playbook1.yml
```

## Callback Plugins

Callback plugins โดยค่าเริ่มต้นเท่ากับ "Skippy" จะมีรูปแบบ
```
PLAY [Print average marks] ******************************************************

TASK [Gethering Facts] **********************************************************
ok: [localhost]

PLAY RECAP **********************************************************************
localhost             :ok=2       changed=0       unreachabled=0         failed=0
```

เราสามารถกำหนดเป็นรูปแบบ json โดย
```
export ANSIBLE_STDOUT_CALLBACK=json; ansible-playbook playbook1.yml
```

User Case
- mail
- Hipchat
- Jabber
- Logstash
- Slack
- Timer