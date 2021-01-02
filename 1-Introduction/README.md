# เริ่มต้น Introduction 

## ทบทวนเรื่องของ Ansible (Recap)
### Ansible Control Machine
Ansible ในส่วนของ Control Machine รองรับเฉพาะ Linux เท่านั้น Playbook, Inventory, Modules ตัวอย่างการติดตั้ง

บน Fedora 
```
yum install ansible
```
บน Ubuntu
```
apt-get install ansible
```
บน python pip
```
pip install ansible
```

หรือในส่วนอื่นๆ 
- Install from source on GIT
- Build RPM yourself

### Inventory Files

```
# Sample Inventory File

web ansible_host=server1.company.com  ansible_connection=ssh ansible_user=root
db ansible_host=server2.company.com  ansible_connection=winrm ansible_user=admin
mail ansible_host=server3.company.com  ansible_connection=ssh ansible_ssh_pass=P@#
web2 ansible_host=server4.company.com  ansible_connection=winrm

localhost ansible_connection=localhost

```
Inventory Parameters:
- ansible_connection - ssh/winrm/localhost
- ansible_port - 22/5986
- ansible_user - root/administrator
- ansible_ssh_pass - Password

ถ้าเก็บข้อมูลแบบต้องการ Security ก็ใช้ Ansible Vault โลด

### เรื่องของ Modules
- System
- Commands
- Files
- Database
- Cloud
- WIndows
- Another...

### เรื่องของ Variable
```
#sample Ansible Playbook.yml

- 
    name: Set Firewall Configuration
    hosts: web
    tasks:
        - 
            firewalld:
                service: https
                permanent: true
                state: enabled
        - 
            firewalld:
                port: '{{ http_port }}'/tcp
                permanent: true
                state: disabled
        - 
            firewalld:
                service: '{{ snmp_port }}'/udp
                permanent: true
                state: disabled
        - 
            firewalld:
                port: '{{ inter_ip_range }}'/24
                Zone: Internal
                state: enabled                            
```
Sample Inventory File
```
web http_port=8081 snmp_port=161-162 inter_ip_range=192.0.2.0
```
Sample Variable File - web.yml
```
http_port: 8081
snmp_port: 161-162
inter_ip_range: 192.0.2.0
```

Jinja2 Templating
```
source: '{{ inter_ip_range }}'
```

### เรื่องของเงื่อนไข (Conditional)

Sample Inventory File
```
web1 ansible_host=web1.company.com ansible_connection=ssh ansible_ssh_pass=P@ssW
db ansible_host=db.company.com ansible_connection=winrm ansible_password=P@s
web2 ansible_host=web3.company.com ansible_connection=ssh ansible_ssh_pass=P@ssW

# Group
[all_servers] 
web1
db
web2

[db_servers]
db

[web_servers]
web1
web2
```

Sample Ansible Playbook1.yml
```
- 
    name: Start services
    hosts: all_servers
    tasks:
        -
            service: name=mysql state=started
            when: ansible_host == "db.company.com"
        -
            service: name=httpd state=started
            when: ansible_connection == "web1.company.com" or
                        ansible_connection == "web2.company.com"

```

### เรื่องของ Loops

Sample Ansible Playbook1.yml
```
- 
    name: Install Packages
    hosts: localhost
    tasks:
        -
            yum: name='{{ item }}' state=present
            with_items:
                - httpd
                - binutils
                - glibc
                - ksh
                - libaio
                - libXext
                - gcc
                - make
                - sysstat
                - unixODBC
                - mongodb
                - nodejs
                - grunt
```

## ในการ Setup Environement
- VMs โดยใช้ Virtual Box หรือ VMware Workstation
- Docker
- Vagrant

เข้าไปที่ vagrant-labs

```
vagrant up
```

จากนั้นเข้าไปที่ master 
```
vagrant ssh master
mkdir ping-test
cd $_
```
ติดตั้ง ansible บน master 
```
sudo yum install epel-release -y
sudo yum install ansible -y

ansible --version
```
ทำการสร้างไฟล์​ inventory.txt
```
target1 ansible_host=192.168.55.21 ansible_connection=ssh ansible_user=root ansible_ssh_pass=vagrant
target2 ansible_host=192.168.55.22 ansible_connection=ssh ansible_user=root ansible_ssh_pass=vagrant
```
จากนั้นทำการทดสอบ test ping 
```
[vagrant@master ping-test]$ ansible all -m ping -i inventory.txt 
target2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
target1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
[vagrant@master ping-test]$
```

### ตัวอย่าง Docker Image ubuntu ssh enabled
The Docker file used to create the ubuntu-ssh-enabled Docker image is located here.
https://github.com/mmumshad/ubuntu-ssh-enabled 

Run the container:
```
docker run -d mmumshad/ubuntu-ssh-enabled
```
Identify the Internal IP
```
docker inspect <container-id-name>
```
SSH
```
ssh <container-ip>
```
Username: root

Password: Passw0rd

เข้าไปที่ master 
```
vagrant ssh master
mkdir docker-test-ping
cd $_

# Install docker on node
sudo curl -fsSL https://get.docker.com | sh -
sudo usermod -aG docker vagrant
sudo systemctl start docker
su - vagrant

docker run -it -d mmumshad/ubuntu-ssh-enabled
docker run -it -d mmumshad/ubuntu-ssh-enabled
docker run -it -d mmumshad/ubuntu-ssh-enabled

docker inspect <docker-id>   -------เพื่อหา ip address ในการกำหนด inventory 
```