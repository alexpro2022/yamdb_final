import re
from django.core.exceptions import ValidationError
from django.utils import timezone


REGEX = r'[\w.@+-]+'


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            f'ОШИБКА: Указанный год публикации {year} больше текущего')
    return year


def validate_username(username):
    if username == 'me':
        raise ValidationError(f'Неверное имя пользователя: "{username}"')
    invalid_symbols = ''.join(set(re.sub(REGEX, '', username)))
    if invalid_symbols:
        raise ValidationError(
            f'Неверные символы {invalid_symbols} '
            f'в имени пользователя: "{username}"')
    return username


class ValidateUsernameMixin:
    def validate_username(self, username):
        return validate_username(username)
