from rest_framework import exceptions


def validate_even_boards(value):
    if value % 2 != 0:
        raise exceptions.ValidationError('Number of boards to play must be even.')
