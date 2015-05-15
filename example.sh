#!/bin/bash

# Cleanup all containers
fab -H mongo1.mycanvas stop_and_remove_mongodb
fab -H mongo1.mycanvas remove_mongodb_data
fab -H mongo1.mycanvas stop_and_remove_weave

fab -H mongo2.mycanvas stop_and_remove_mongodb
fab -H mongo2.mycanvas remove_mongodb_data
fab -H mongo2.mycanvas stop_and_remove_weave

fab -H mongo3.mycanvas stop_and_remove_mongodb
fab -H mongo3.mycanvas remove_mongodb_data
fab -H mongo3.mycanvas stop_and_remove_weave


# Primary container
fab -H mongo1.mycanvas run_weave
fab -H mongo1.mycanvas build_mongodb
fab -H mongo1.mycanvas run_mongodb:ip="10.2.0.1"
echo "Lets wait 10 seconds and make sure mongodb is started..."
sleep 10
fab -H mongo1.mycanvas initiate_rs
fab -H mongo1.mycanvas fix_servername:ip="10.2.0.1"

# Second container
fab -H mongo2.mycanvas run_weave:ip="10.0.2.200"
fab -H mongo2.mycanvas build_mongodb
fab -H mongo2.mycanvas run_mongodb:ip="10.2.0.2"

# Third container
fab -H mongo3.mycanvas run_weave:ip="10.0.2.200"
fab -H mongo3.mycanvas build_mongodb
fab -H mongo3.mycanvas run_mongodb:ip="10.2.0.3"

echo "Lets wait 10 seconds and make sure mongodb is started..."
sleep 10

# Add members to primary
fab -H mongo1.mycanvas add_rs_member:ip="10.2.0.2"
fab -H mongo1.mycanvas add_rs_member:ip="10.2.0.3"
