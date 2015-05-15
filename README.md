# easy-replica-mongo
Replica Set MongoDB Fabric Docker/Weave Fabric deploy scripts


### Installation on local machine
```
$ virtualenv easy-replica-mongo
$ cd easy-replica-mongo
$ git clone git@github.com:tedostrem/easy-replica-mongo.git app
$ source bin/activate
$ cd app
$ pip install -r requirements.txt
$ ssh-add <all of your keyfiles>
```

OK now we can start deploying stuff..
 

#### On all
```
$ fab -H <host> docker.build_socat
$ fab -H <host> docker.install_docker
$ fab -H <host> install_weave
```

#### Primary
```
$ fab -H <primary_host> run_weave
$ fab -H <primary_host> build_mongodb
$ fab -H <primary_host> run_mongodb:ip="10.2.0.1"

# Here we need to sleep about 10 seconds until mongodb is started

$ fab -H <primary_host> initiate_rs
$ # Server name cant be docker container id
$ fab -H <primary_host> fix_servername:ip="10.2.0.1"
```

#### Secondaries
```
$ fab -H <secondary_host> run_weave:ip="<primary ip>"
$ fab -H <secondary_host> build_mongodb
$ fab -H <secondary_host> run_mongodb:ip="10.2.0.<1+n>"
# Remember to sleep a bit here
```

#### Initiate replica set and add members 
```
$ fab -H <primary_host> initiate_rs

# Per host
$ fab -H <primary_host> add_rs_member:ip="<secondary_weaver_ip>"
```

## Example bash script
```
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
```
