#!/usr/bin/env python

# 'SNOW' refers to ServiceNow

# Ensure that the following environment variables are set prior to running this script:

# Base URL of your ServiceNow API service like "https://_DOMAIN_/api"
# export SNOW_BASE_URL="_VALUE_HERE_"

# Set ServiceNow credentials
# export SNOW_USERNAME="_VALUE_HERE_"
# export SNOW_PASSWORD="_VALUE_HERE_"

# API calls to Service Now are slow. For this reason, we cache the results
# of an API call. Set this to the path you want cache files to be written
# to. Two files will be written to this directory:
#   - ansible-snow.cache
#   - ansible-snow.index
# export SNOW_CACHE_DIR="~/.ansible"

# The number of seconds a cache file is considered valid. After these many
# seconds, a new API call will be made, and the cache file will be updated.
# To disable the cache, set this value to 0
# export SNOW_CACHE_MAX_AGE="300"

from __future__ import print_function
from time import time
import os, sys, json
import requests

''' 
   Function to initialize the 'inventory' dictionary, 
   where 'inventory' holds the results received from ServiceNow
'''
def empty_inventory():
    # Initialize/structurize your 'inventory' dictionary here
    os_type = '_OS_TYPE_VALUE_HERE_' # Example value: 'ubuntu'
    inventory = {}
    inventory['_meta'] = { 'hostvars': {} }
    inventory[os_type] = {}
    inventory[os_type]['vars'] = {}
    inventory[os_type]['vars']['ansible_shell_type'] = 'csh'
    return inventory

def main(args):
    evars = get_env_vars()
    username = evars['username']
    password = evars['password']
    base_url = evars['base_url']

    ''' 
       QUERY PARAMETER DECLARATION SECTION
          - Declare and/or initialize the parameters you will need for generating servers_url
          - For example:
               To look for entries that belong to a specific department, you could do-
                  department_id = "_DEPT_ID_HERE_"
    '''

    # This is the sys_id for a specific IT Function
    it_function_id = "_IT_FUNCTION_ID_HERE_"

    # Life Cycle Status == In Production
    life_cycle_status_id = "_LIFE_CYCLE_STATUS_ID_HERE_"

    # Operational Status == Production
    operational_status_id = "_OPERATIONAL_STATUS_ID_HERE__"
  
    ''' 
       QUERY ENDPOINT GENERATION SECTION
          - Generate your query endpoint in servers_url using above defined parameters
          - This endpoint will be hit to fetch results from ServiceNow
          - For example:
               Your query endpoint might look like-
                  servers_url = base_url + '/' + '?department=' + department_id
    ''' 
    servers_url = '_QUALIFIED_QUERY_URL_HERE_'
   
    cache_path = get_cache_path(evars['cache_dir'])
    cache_max_age = evars['cache_max_age']
    if not is_cache_valid(cache_path,cache_max_age):
        inventory = get_inventory(servers_url,username,password)
        update_cache(inventory,cache_path)
    else:
        inventory = get_inventory_from_cache(cache_path)

    print(json.dumps(inventory, indent=4))

def get_env_vars():
    evars = {}
    try:
        evars['username'] = os.environ['SNOW_USERNAME']
        evars['password'] = os.environ['SNOW_PASSWORD']
        evars['base_url'] = os.environ['SNOW_BASE_URL']
        evars['cache_dir'] = os.environ['SNOW_CACHE_DIR']
        evars['cache_max_age'] = os.environ['SNOW_CACHE_MAX_AGE']
    except KeyError as e:
        print("ERROR: environment variable %s is not defined" % e, file=sys.stderr)
        sys.exit(-1)

    return evars

def get_cache_path(cache_dir):
    cache_dir = os.path.expanduser(cache_dir)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    return cache_dir + "/ansible-snow.cache"


def is_cache_valid(cache_path,cache_max_age):
    ''' Determines if the cache files have expired, or if it is still valid '''

    if os.path.isfile(cache_path):
        mod_time = os.path.getmtime(cache_path)
        current_time = time()
        if (mod_time + int(cache_max_age)) > current_time:
            return True

    return False

def get_inventory(servers_url,username,password):
    inventory = empty_inventory()
    it_function_id = "_VALUE_HERE_"

    response = requests.get(
      servers_url,
      auth=(username,password),
      headers={"Accept":"application/json"}
    )

    if response.status_code != 200:
        print(
            'Status:', response.status_code,
            'Headers:', response.headers,
            'Error Response:', response.json()
        )
        exit()

    servers = response.json()['result']

    ''' 
       PARSING LOGIC: To filter the required servers from GET response 'server'
                      You can customize this filtering according to your business needs.
                      Make sure to replace the _FILTER_CONDITION_HERE_ below with real value.
                      Then you can add required servers to the 'inventory' by calling
                       'add_server_to_host_group()' function
    '''
    for server in servers:
        if _FILTER_CONDITION_HERE_: 
            add_server_to_host_group(
                server['os'].lower(),
                server['name'],
                inventory
            )
    # return the fully-loaded, filtered inventory
    return inventory

def update_cache(data,filename):
    ''' Writes data in JSON format to a file '''

    json_data = json.dumps(data, sort_keys=True, indent=2)
    cache = open(filename, 'w')
    cache.write(json_data)
    cache.close()

def get_inventory_from_cache(cache_path):
    ''' Reads the inventory from the cache file and returns it as JSON '''

    cache = open(cache_path, 'r')
    json_inventory = cache.read()
    return json.loads(json_inventory)

def add_server_to_host_group(group, name, inventory):
    host_group = inventory.get(group, {})
    hosts = host_group.get('hosts', [])
    hosts.append(name)
    host_group['hosts'] = hosts
    inventory[group] = host_group

if __name__ == "__main__":
    main(sys.argv)
