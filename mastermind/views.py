from rest_framework import viewsets

from mastermind import filters
from mastermind import models
from mastermind import serializers


class GameViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'trace']
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer


class BoardViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    queryset = models.Board.objects.all()
    serializer_class = serializers.BoardSerializer
    filterset_class = filters.BoardFilterSet


class GuessViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    queryset = models.Guess.objects.all()
    serializer_class = serializers.GuessSerializer
    filterset_class = filters.GuessFilterSet
