# easy-replica-mongo
Replica Set MongoDB Fabric Docker/Weave Fabric deploy deploy 

### On all
```
$ fab -H <host> docker.build_socat
$ fab -H <host> docker.install_docker
$ fab -H <host> install_weave
```

### Primary
```
$ fab -H <primary_host> run_weave
$ fab -H <primary_host> build_mongodb
$ fab -H <primary_host> run_mongodb:ip="10.2.0.1"
$ fab -H <primary_host> initiate_replica_set
```

### Secondaries
```
$ fab -H <secondary_host> run_weave:ip="<primary ip>"
$ fab -H <secondary_host> build_mongodb
$ fab -H <secondary_host> run_mongodb:ip="10.2.0.2"
```

### Initiate replica set and add memebers
```
$ fab -H <primary_host> initiate_rs

# Per host
$ fab -H <primary_host> add_rs_member:ip="<secondary_weaver_ip>"
```
