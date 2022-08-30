from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year


MODEL_REPR_TEXT_SIZE = 100
USERNAME_MAX_LEN = 150
EMAIL_MAX_LEN = 254
CONFIRMATION_CODE_SIZE = 6
RESET_CONFIRMATION_CODE = 'N' * CONFIRMATION_CODE_SIZE


class User(AbstractUser):
    ADMIN, MODERATOR, USER = 'admin', 'moderator', 'user'
    ROLES = ((ADMIN, 'Администратор'),
             (MODERATOR, 'Модератор'),
             (USER, 'Пользователь'))
    username = models.CharField(
        max_length=USERNAME_MAX_LEN, unique=True,
        validators=[validate_username])
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name='first name')
    last_name = models.CharField(
        blank=True, max_length=150, verbose_name='last name')
    email = models.EmailField(max_length=EMAIL_MAX_LEN, unique=True)
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES, default=USER)
    bio = models.TextField('Биография', null=True, blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=CONFIRMATION_CODE_SIZE, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username


class AbstractCategoryGenre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(AbstractCategoryGenre):
    class Meta(AbstractCategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractCategoryGenre):
    class Meta(AbstractCategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField('Название')
    year = models.PositiveSmallIntegerField(
        'Год публикации', validators=[validate_year])
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='titles', verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class AbstractReviewComment(models.Model):
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:MODEL_REPR_TEXT_SIZE]


class Review(AbstractReviewComment):
    title = models.ForeignKey(
        Title, models.CASCADE, verbose_name='Отзыв')
    score = models.PositiveSmallIntegerField('Оценка', validators=[
        MinValueValidator(1, 'Минимальное значение = 1'),
        MaxValueValidator(10, 'Максимальное значение = 10')])

    class Meta(AbstractReviewComment.Meta):
        default_related_name = "reviews"
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='author_unique_review')]


class Comment(AbstractReviewComment):
    review = models.ForeignKey(
        Review, models.CASCADE, verbose_name='Комментарий')

    class Meta(AbstractReviewComment.Meta):
        default_related_name = "comments"
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
