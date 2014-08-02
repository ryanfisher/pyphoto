from fabric.api import *
from fabric.contrib import django, project
from fabric.colors import green, red

# django.settings_module('photos.project.settings.production')
# from django.conf import settings

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
        sudo('cd /mnt/current && pip install -r requirements.txt')
        sudo('python /mnt/current/manage.py migrate')
        print(green('master pushed to production'))
        # local('python /home/ryan/Dev/ryanfisher/photo/manage.py collectstatic --noinput --settings=project.settings.production')
        project.upload_project(
            remote_dir = '/mnt/current',
            local_dir = '/home/ryan/Dev/ryanfisher/photo/static',
            use_sudo = True
        )
        print(red('updating static files'))
        sudo('restart uwsgi')
