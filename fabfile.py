from fabric.api import env, task, run, put
from dockerfabric.apiclient import docker_fabric
from dockerfabric import tasks as docker
from dockermap.api import DockerFile

env.docker_tunnel_local_port = 22024


@task
def install_weave():
    run(('sudo wget -O /usr/local/bin/weave '
         'https://github.com/weaveworks/weave/releases/download/'
         'latest_release/weave'))
    run('sudo chmod a+x /usr/local/bin/weave')


@task
def build_mongodb():
    with DockerFile('ubuntu:latest',
                    maintainer='Ted Ostrem, ted.ostrem@gmail.com') as df:
        df.prefix('ENV', 'DEBIAN_FRONTEND', 'noninteractive')
        df.run('apt-get update')
        df.run('apt-get -y upgrade')
        df.run(('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 '
                '--recv 7F0CEB10 && '
                'echo "deb http://repo.mongodb.org/apt/ubuntu '
                '"$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | '
                'tee /etc/apt/sources.list.d/mongodb-org-3.0.list && '
                'apt-get update && '
                'apt-get install -y mongodb-org'))
        df.add_volume('/data/db')
        df.prefix('ENV', 'REPLSET', 'rs0')
        df.prefix('ENV', 'AUTH', 'no')
        df.prefix('ENV', 'STORAGE_ENGINE', 'wiredTiger')
        df.prefix('ENV', 'JOURNALING', 'yes')
        df.add_file('run.sh', '/run.sh')
        df.add_file('set_mongodb_password.sh', '/set_mongodb_password.sh')
        df.prefix('EXPOSE', '27017', '28017')
        df.prefix('CMD', './run.sh')
        docker_fabric().build_from_file(df,
                                        'tedostrem/mongodb',
                                        add_latest_tag=True,
                                        rm=True)


@task
def remove_mongodb_data():
    run('sudo rm -frv /data/mongodb')


@task
def stop_and_remove_mongodb():
    run('docker stop mongodb && docker rm mongodb')


@task
def stop_and_remove_weave():
    run('docker stop weave && docker rm weave')


@task
def run_weave(ip=None):
    if ip:
        run('weave launch %s' % (ip, ))
    else:
        run('weave launch')


@task
def run_mongodb(ip):
    run(('C=$(weave run %s/24 --name mongodb -d -p 27017:27017 -p 28017:28017 '
         '-v /data/mongodb:/data/db tedostrem/mongodb)') % (ip, ))


@task
def fix_servername(ip):
    query = ('cfg = rs.conf();\n'
             'cfg.members[0].host = "%s:27017";\n'
             'rs.reconfig(cfg);\n'
             'rs.status();\n') % (ip, )
    f = open('reconf.js', 'w')
    f.write(query)
    f.close()
    put('reconf.js', '~/reconf.js')
    run('sudo mv ~/reconf.js /data/mongodb/reconf.js')
    run('docker exec mongodb cat /data/db/reconf.js')
    run('docker exec mongodb mongo --eval "printjson(load(\'/data/db/reconf.js\'))"')


@task
def initiate_rs():
    run('docker exec mongodb mongo --eval "printjson(rs.initiate())"')


@task
def add_rs_member(ip):
    run('docker exec -it mongodb mongo --eval "printjson(rs.add("%s"))"' %
        (ip, ))
