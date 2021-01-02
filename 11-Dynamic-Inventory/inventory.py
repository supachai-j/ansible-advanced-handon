#! /usr/bin/env python

import json

# Get inventory data from source - CMDB or any other API
def get_inventory_data():
    return {
        "databases": {
            "hosts": ["web_server"],
            "vars": { 
                "ansible_ssh_pass":"vagrant",
                "ansible_ssh_host": "192.168.55.29"
            }
        },
        "web": {
            "hosts": ["db_server"],
            "vars": {
                "ansible_ssh_pass":"vagrant",
                "ansible_ssh_host": "192.168.1.30"
            }
        }
    }
# Default main function
if __name__ == "__main__":
    inventory_data = get_inventory_data()
    print(json.dumps(inventory_data))