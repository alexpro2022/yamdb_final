from django_filters import rest_framework as filters

from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    name = filters.CharFilter('name', 'icontains')
    category = filters.CharFilter('category__slug', 'icontains')
    genre = filters.CharFilter('genre__slug', 'icontains')

    class Meta:
        model = Title
        exclude = ('description',)
