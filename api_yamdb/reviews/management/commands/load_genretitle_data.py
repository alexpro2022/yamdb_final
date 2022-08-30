from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Genre, Title, GenreTitle
from ._utils import info


class Command(BaseCommand):
    CLS = GenreTitle
    FILE_NAME = 'genre_title'
    help = f'Loads data from {FILE_NAME}.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'static/data/{self.FILE_NAME}.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                genre=Genre.objects.get(pk=row['genre_id']))
            instance.save()
