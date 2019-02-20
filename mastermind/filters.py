from django_filters import rest_framework as filters

from mastermind import models


class GuessFilterSet(filters.FilterSet):
    class Meta:
        model = models.Guess
        fields = ('board', 'number')

    game = filters.NumberFilter(field_name='board__game')
    ordering = filters.OrderingFilter(fields=('board__number', 'number'))


class BoardFilterSet(filters.FilterSet):
    class Meta:
        model = models.Board
        fields = ('game', 'number', 'winner')

    ordering = filters.OrderingFilter(fields=('number',))
