from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import (
    USERNAME_MAX_LEN, EMAIL_MAX_LEN, CONFIRMATION_CODE_SIZE,
    Category, Comment, Genre, Review, Title, User)
from reviews.validators import ValidateUsernameMixin, validate_year


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        'slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        'slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, year):
        return validate_year(year)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError(
                    'Пользователю разрешен только один отзыв на произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(ValidateUsernameMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class MeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(ValidateUsernameMixin, serializers.Serializer):
    username = serializers.CharField(max_length=USERNAME_MAX_LEN)
    email = serializers.EmailField(max_length=EMAIL_MAX_LEN)


class JWTTokenSerializer(ValidateUsernameMixin, serializers.Serializer):
    username = serializers.CharField(max_length=USERNAME_MAX_LEN)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_SIZE)
