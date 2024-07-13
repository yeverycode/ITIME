from django.core.management.base import BaseCommand
from techtime.models import Board

class Command(BaseCommand):
    help = 'Create default board'

    def handle(self, *args, **kwargs):
        if not Board.objects.filter(board_id=1).exists():
            Board.objects.create(board_id=1, name='Default Board')
            self.stdout.write(self.style.SUCCESS('Successfully created default board'))
        else:
            self.stdout.write(self.style.WARNING('Default board already exists'))
