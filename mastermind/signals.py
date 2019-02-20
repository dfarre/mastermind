import collections

from django import dispatch
from django.conf import settings
from django.db.models import signals

from mastermind import models


@dispatch.receiver(signals.post_save, sender=models.Guess)
def handle_new_guess(sender, instance, **kwargs):
    def set_board_winner(guess):
        if guess.feedback == ['F']*settings.CODE_SIZE:
            guess.board.winner = 'B'
            guess.board.save()
        elif guess.number == guess.board.game.board_size:
            guess.board.winner = 'M'
            guess.board.save()

    def score(guess):
        guess.board.game.breaker_score += collections.Counter(guess.feedback)['F']
        guess.board.game.maker_score += 2 if guess.board.winner == 'M' else 1
        guess.board.game.save()

    set_board_winner(instance)
    score(instance)
