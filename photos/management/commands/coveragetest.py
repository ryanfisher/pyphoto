from django.core.management.base import BaseCommand

import subprocess


class Command(BaseCommand):
    help = "Runs test code and creates coverage report"

    def handle(self, *args, **options):
        result = subprocess.call("coverage run manage.py test" +
                                 " --settings=project.settings.test",
                                 shell=True)
        if result == 0:
            subprocess.call('coverage html --include="$SITE_URL*"' +
                            '--omit="admin.py"', shell=True)
        else:
            self.stdout.write("TEST FAILURES")
