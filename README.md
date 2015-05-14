# easy-replica-mongo
Replica Set MongoDB Fabric Docker/Weave Fabric deploy scirpts

### On all
```
$ fab -H <host> docker.build_socat
$ fab -H <host> docker.install_docker
$ fab -H <host> install_weave
```

### Primary
```
$ fab -H <host> run_weave
$ fab -H <host> build_mongodb
$ fab -H <host> run_mongodb:ip="10.2.0.1"
$ fab -H <host> initiate_replica_set
```

### Set secondaries
```
$ fab -H <host> run_weave:ip="<primary ip>"
$ fab -H <host> run_mongodb:ip="10.2.0.2"
```
