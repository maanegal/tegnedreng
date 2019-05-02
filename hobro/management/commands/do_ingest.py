from django.core.management.base import BaseCommand
from hobro import ingest


class Command(BaseCommand):
    help = 'Load content to db'

    def handle(self, *args, **kwargs):
        pt = ingest.temp_path
        self.stdout.write("Loading from %s" % pt)
        ingest.folder_loader(pt)
