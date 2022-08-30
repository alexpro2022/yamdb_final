from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,
    TitleViewSet, UserViewSet, SignUpView, ObtainTokenView)

VERSION = 'v1'

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns_auth = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', ObtainTokenView.as_view(), name='token'),
]

urlpatterns = [
    path(f'{VERSION}/', include(router_v1.urls)),
    path(f'{VERSION}/', include(urlpatterns_auth))
]
