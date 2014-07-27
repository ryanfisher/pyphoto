from fabric.api import *
from fabric.contrib import django
from fabric.colors import green, red

def prod():
    '''The production server'''
    env.host_string = 'ec2-54-91-69-59.compute-1.amazonaws.com'
    env.user = 'ec2-user'
    env.key_filename = '~/.ec2/photo-key.pem'


@task
def deploy_prod():
    prod()
    git_path = "/home/ec2-user/photo/photo.git"
    process = "deploying"

    print(red("Beginning Deploy:"))
    with cd(git_path):
        print(red('pushing master to production'))
        local('git push production master')
        sudo('git --work-tree=/mnt/current checkout -f master')
        run('source /opt/apps/photo-env/bin/activate')
        run('cd /mnt/current && pip install -r requirements.txt')
        print(green('master pushed to production'))
        print(red('NEED TO GET COLLECTSTATIC WORKING'))
        sudo('restart uwsgi')
