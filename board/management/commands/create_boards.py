from django.core.management.base import BaseCommand
from board.models import Board

class Command(BaseCommand):
    help = 'Create initial boards'

    def handle(self, *args, **kwargs):
        boards = [
            '자유게시판', '졸업생게시판', '새내기게시판', '취업,진로 게시판',
            '정보게시판', '홍보게시판', '학생회게시판', '동아리게시판'
        ]

        for board_name in boards:
            board, created = Board.objects.get_or_create(name=board_name, defaults={'description': f'{board_name} 설명'})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created board: {board_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Board already exists: {board_name}'))
