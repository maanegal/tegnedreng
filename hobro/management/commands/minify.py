from django.core.management.base import BaseCommand
from hobro.helpers import minify_resources


class Command(BaseCommand):
    help = 'Minify css and js'

    def handle(self, *args, **kwargs):
        minify_resources()
