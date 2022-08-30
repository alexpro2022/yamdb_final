from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Category, Title
from ._utils import info


class Command(BaseCommand):
    CLS = Title
    FILE_NAME = CLS.__name__.lower()
    help = f'Loads data from {FILE_NAME}.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'static/data/{self.FILE_NAME}.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=row['category']))
            instance.save()
