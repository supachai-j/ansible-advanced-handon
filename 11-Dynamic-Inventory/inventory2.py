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
def read_cli_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host', action='store')
    args = parser.parser_agrs()

# Default main function
if __name__ == "__main__":
    global args
    read_cli_args()
    inventory_data = get_inventory_data()
    if args and args.list:
        print(json.dump(inventory_data))
    elif args.host: 
        print(json.dumps({ '_meta': { 'hostvars': {}}}))