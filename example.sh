#!/bin/bash

# Cleanup all containers
fab -H mongo1 stop_and_remove_mongodb
fab -H mongo1 remove_mongodb_data
fab -H mongo1 stop_and_remove_weave

fab -H mongo2 stop_and_remove_mongodb
fab -H mongo2 remove_mongodb_data
fab -H mongo2 stop_and_remove_weave

fab -H mongo3 stop_and_remove_mongodb
fab -H mongo3 remove_mongodb_data
fab -H mongo3 stop_and_remove_weave


# Primary
fab -H mongo1 run_weave
fab -H mongo1 build_mongodb
fab -H mongo1 run_mongodb:ip="10.2.0.1"
echo "Lets wait 10 seconds and make sure mongodb is started..."
sleep 10
fab -H mongo1 initiate_rs
fab -H mongo1 fix_servername:ip="10.2.0.1"

# Second
fab -H mongo2 run_weave:ip="10.0.2.200"
fab -H mongo2 build_mongodb
fab -H mongo2 run_mongodb:ip="10.2.0.2"

# Third
fab -H mongo3 run_weave:ip="10.0.2.200"
fab -H mongo3 build_mongodb
fab -H mongo3 run_mongodb:ip="10.2.0.3"

echo "Lets wait 10 seconds and make sure mongodb is started..."
sleep 10

# Add members to primary
fab -H mongo1 add_rs_member:ip="10.2.0.2"
fab -H mongo1 add_rs_member:ip="10.2.0.3"
