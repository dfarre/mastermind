from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.postgres import fields
from django.db import models

from mastermind import validators


class BaseGame(models.Model):
    round_object = ''

    class Meta:
        abstract = True

    def round(self):
        getattr(self, f'{self.round_object}_set').order_by('number').last()


class Round(models.Model):
    colors = (('R', 'Red'), ('O', 'Orange'), ('Y', 'Yellow'),
              ('G', 'Green'), ('B', 'Blue'), ('P', 'Purple'))

    code = fields.ArrayField(
        models.CharField(max_length=1, choices=colors), size=settings.CODE_SIZE)
    number = models.PositiveIntegerField(blank=True)

    class Meta:
        abstract = True


class Game(BaseGame):
    round_object = 'board'

    codebreaker = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    last_board = models.PositiveIntegerField(validators=[validators.validate_even_boards])
    board_size = models.PositiveIntegerField(default=12)
    breaker_score = models.PositiveIntegerField(default=0)
    maker_score = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'game'

    def __str__(self):
        sizes = f'{self.last_board} boards of {self.board_size} guesses'
        score = f'{self.breaker_score} points against {self.maker_score}'

        return f'{sizes} - breaker {self.codebreaker} with {score}'

    @property
    def rankings(self):
        return sorted({'Breaker': self.breaker_score, 'Maker': self.maker_score}.items(),
                      key=lambda item: item[1])


class Board(BaseGame, Round):
    round_object = 'guess'

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    winner = models.CharField(
        max_length=1, choices=(('B', 'Breaker'), ('M', 'Maker'), ('', '')))

    class Meta:
        db_table = 'board'

    def __str__(self):
        return f'{self.number} of {self.game} - {"".join(self.code)} hidden'


class Guess(Round):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    feedback = fields.ArrayField(models.CharField(max_length=1, choices=(
        ('F', 'Full'), ('C', 'Color'), ('', ''))),
        size=settings.CODE_SIZE, blank=True)

    class Meta:
        db_table = 'guess'
        indexes = (models.Index(fields=('board', 'number')),)

    def __str__(self):
        return f'{self.number} of board {self.board} - {"".join(self.code)}'
