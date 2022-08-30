from django.core.management import BaseCommand

from .load_category_data import Command as load_categories
from .load_genre_data import Command as load_genres
from .load_users_data import Command as load_users
from .load_title_data import Command as load_titles
from .load_genretitle_data import Command as load_genres_titles
from .load_comment_data import Command as load_comments
from .load_review_data import Command as load_reviews


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_users().handle()
        load_categories().handle()
        load_genres().handle()
        load_titles().handle()
        load_genres_titles().handle()
        load_reviews().handle()
        load_comments().handle()
