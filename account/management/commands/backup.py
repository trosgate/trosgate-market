from django.core.management.base import BaseCommand
from django.core import management
import os
import datetime


class Command(BaseCommand):
    help = 'Creates a backup of the database and media files.'

    def handle(self, *args, **options):
        # Backup the database
        db_name = management.settings.DATABASES['default']['trosgate']
        db_filename = '{}-{}.json'.format(db_name, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        management.call_command('dumpdata', '--indent=4', '--output={}'.format(db_filename))
        self.stdout.write(self.style.SUCCESS('Successfully backed up database to {}'.format(db_filename)))

        # Backup the media files
        media_root = management.settings.MEDIA_ROOT
        media_filename = 'media-{}.tar.gz'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        media_command = 'tar -zcvf {} {}'.format(media_filename, media_root)
        os.chdir(media_root)
        os.system(media_command)
        os.chdir('..')
        self.stdout.write(self.style.SUCCESS('Successfully backed up media files to {}'.format(media_filename)))
