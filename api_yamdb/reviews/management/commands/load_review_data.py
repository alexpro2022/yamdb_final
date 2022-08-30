from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Review, Title, User
from ._utils import info


class Command(BaseCommand):
    CLS = Review
    FILE_NAME = CLS.__name__.lower()
    help = f'Loads data from {FILE_NAME}.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'static/data/{self.FILE_NAME}.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date'])
            instance.save()
