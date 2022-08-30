import random

from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, permissions, status, views, viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import FROM_EMAIL
from reviews.models import (
    Category, Genre, Review, Title, User,
    CONFIRMATION_CODE_SIZE, RESET_CONFIRMATION_CODE)
from .filters import TitlesFilter
from .mixins import LCDViewSet
from .permissions import IsAdmin, ReadOnly, IsAuthorOrStaffOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    MeSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    JWTTokenSerializer,
    UserSerializer)


class CategoryGenreViewSet(LCDViewSet):
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitlesFilter
    ordering_fields = ('rating',)
    # ordering = ('-rating',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(('GET', 'PATCH'), False,
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            return Response(
                MeSerializer(request.user).data, status=status.HTTP_200_OK)
        serializer = MeSerializer(request.user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data)
        except IntegrityError:
            raise ValidationError('ОШИБКА - ник или мейл уже заняты')
        user.confirmation_code = ''.join(
            random.sample('0123456789', CONFIRMATION_CODE_SIZE))
        user.save(update_fields=['confirmation_code'])
        send_mail(
            'YaMDb registration',
            f'Код подтверждения {user.confirmation_code}.',
            FROM_EMAIL, [user.email])
        return Response(serializer.data, status.HTTP_200_OK)


class ObtainTokenView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, confirmation_code = serializer.validated_data.values()
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == RESET_CONFIRMATION_CODE:
            raise ValidationError('Получите код подтверждения')
        if user.confirmation_code != confirmation_code:
            raise ValidationError('Неправильный код подтверждения')
        user.confirmation_code = RESET_CONFIRMATION_CODE
        user.save(update_fields=['confirmation_code'])
        return Response(
            {"token": str(AccessToken.for_user(user))}, status.HTTP_200_OK)
