import collections
import random

from django.conf import settings

from rest_framework import exceptions
from rest_framework import serializers

from mastermind import models


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = '__all__'
        read_only_fields = ('codebreaker', 'breaker_score', 'maker_score')

    def create(self, validated_data):
        validated_data['codebreaker'] = self.context['request'].user

        return super().create(validated_data)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = '__all__'
        read_only_fields = ('number', 'code', 'winner')

    def validate_user(self, data):
        if self.context['request'].user != data['game'].codebreaker:
            raise exceptions.ValidationError('Not your game!')

    @staticmethod
    def validate_game_state(data):
        board = data['game'].round()

        if board:
            if not board.winner:
                raise exceptions.ValidationError(
                    f'You have {data["game"].board_size - board.round().number} '
                    f'guess(es) left on board {board.number}!')
            elif board.number == data['game'].last_board:
                (l, ls), (w, ws) = data['game'].rankings

                raise exceptions.ValidationError(
                    f'Game is over, all boards completed! {w} {ws} - {l} {ls}')

    def validate(self, data):
        self.validate_user(data)
        self.validate_game_state(data)

        return data

    @staticmethod
    def set_number(data):
        board = data['game'].round()
        data['number'] = board.number + 1 if board else 1

    @staticmethod
    def set_hidden_code(data):
        data['code'] = random.choices(next(zip(*models.Round.colors)), k=settings.CODE_SIZE)

    def create(self, validated_data):
        self.set_number(validated_data)
        self.set_hidden_code(validated_data)

        return super().create(validated_data)


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guess
        fields = '__all__'
        read_only_fields = ('number', 'feedback')

    def validate_user(self, data):
        if self.context['request'].user != data['board'].game.codebreaker:
            raise exceptions.ValidationError('Not your game!')

    @staticmethod
    def validate_board_state(data):
        if data['board'].winner:
            raise exceptions.ValidationError(
                'You already guessed the code!' if data['board'].winner == 'B'
                else 'Board is full, you did not guess the code!')

    def validate(self, data):
        self.validate_user(data)
        self.validate_board_state(data)

        return data

    @staticmethod
    def set_number(data):
        guess = data['board'].round()
        data['number'] = guess.number + 1 if guess else 1

    @staticmethod
    def set_feedback(data):
        match = enumerate(zip(data['code'], data['board'].code))
        fulls = {i: b for i, (b, m) in filter(lambda x: x[1][0] == x[1][1], match)}
        breaker_rest = set(collections.Counter([
            c for i, c in enumerate(data['code']) if i not in fulls]).items())
        maker_rest = set(collections.Counter([
            c for i, c in enumerate(data['board'].code) if i not in fulls]).items())
        colors = breaker_rest & maker_rest
        feedback = ['F']*len(fulls) + ['C']*sum(n for c, n in colors)
        data['feedback'] = feedback + ['']*(settings.CODE_SIZE - len(feedback))

    def create(self, validated_data):
        self.set_number(validated_data)
        self.set_feedback(validated_data)

        return super().create(validated_data)
