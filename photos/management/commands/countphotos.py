from django.core.management.base import BaseCommand, CommandError
from photos.models import Photo

class Command(BaseCommand):
    help = "Counts the number of photos in the database"

    def handle(self, *args, **options):
        photo_count = Photo.objects.count()

        self.stdout.write('There are %s photos in the database' % photo_count)
