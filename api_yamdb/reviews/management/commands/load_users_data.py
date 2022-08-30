from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import User
from ._utils import info


class Command(BaseCommand):
    CLS = User
    FILE_NAME = 'user'
    help = f'Loads data from {FILE_NAME}.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'static/data/{self.FILE_NAME}.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                role=row['role'],
                bio=row['bio'])
            instance.save()
