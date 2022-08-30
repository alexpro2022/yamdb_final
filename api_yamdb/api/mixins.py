from rest_framework import mixins, viewsets


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class LCDViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass
