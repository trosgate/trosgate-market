from django.core.management.base import BaseCommand
from django.core.management import call_command
from account.models import Country, Package, Customer



class Command(BaseCommand):
    help = "this refreshes the system"

    def handle(self, *args, **kwargs):
        
        print('This command is special')

        