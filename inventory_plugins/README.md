# Inventory Plugins
**Service Now Ansible Inventory Script**

This script fetches records from ServiceNow CMDB using REST API that can then be used as an ansible inventory.

This can be useful for those wanting to run ansible playbooks against thousands of servers maintained in ServiceNow CMDB.
This script can then provide you a list of servers from CMDB that can then be used as an ansible inventory.

# Initial Setup
Make sure you set the following environment variables:

1. Base URL of your ServiceNow API service.
  
   For example: "https://_DOMAIN_/api"

   ```export SNOW_BASE_URL="_VALUE_HERE_"```

2. Set ServiceNow credentials

   ```export SNOW_USERNAME="_VALUE_HERE_"```

   ```export SNOW_PASSWORD="_VALUE_HERE_"```

3. Set Cache directory

 API calls to Service Now are slow. For this reason, we cache the results
 of an API call. Set this to the path you want cache files to be written
 to. Two files will be written to this directory:
  - ansible-snow.cache
  - ansible-snow.index
   
  ```export SNOW_CACHE_DIR="~/.ansible"```

4. Set Cache age

 The number of seconds a cache file is considered valid. After these many
 seconds, a new API call will be made, and the cache file will be updated.

 To disable the cache, set this value to 0
 
  ```export SNOW_CACHE_MAX_AGE="300"```

**Note:**
You might be needed to make minor changes in the script like setting up attributes specific to your result requirements.
Comments in the script will guide you through making such minor changes.
