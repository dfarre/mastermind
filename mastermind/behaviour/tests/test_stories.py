import unittest.mock as mock

from bdd_coder.tester import decorators

from django.conf import settings

from . import base


class NewGame(base.BddTester):
    """
    As a codebreaker
    I want to start a new Mastermind game of B boards of G guesses
    In order to play
    """

    @decorators.Scenario(base.steps)
    def test_odd_boards(self):
        """
        When I request a new `game` of "9" boards of "12" guesses
        Then I get a 400 response saying it must be even
        """

    @decorators.Scenario(base.steps)
    def even_boards(self):
        """
        When I request a new `game` of "2" boards of "3" guesses
        Then a game of "2" boards of "3" guesses and me as the codebreaker is created
        """

    def i_request_a_new_game_of__boards_of__guesses(self, *args):
        return self.client.post('/games/', {
            'last_board': int(args[0]), 'board_size': int(args[1])}),

    def i_get_a_400_response_saying_it_must_be_even(self, *args):
        response = self.steps.outputs['game'][-1]

        assert response.status_code == 400
        assert response.json() == {'last_board': ['Number of boards to play must be even.']}

    def a_game_of__boards_of__guesses_and_me_as_the_codebreaker_is_created(self, *args):
        response = self.steps.outputs['game'][-1]
        game = {**response.json()}

        assert response.status_code == 201

        game.pop('id')

        assert game == {
            'last_board': int(args[0]), 'board_size': int(args[1]),
            'codebreaker': self.user.id, 'breaker_score': 0, 'maker_score': 0}


class MakingGuesses(base.BddTester):
    """
    As a codebreaker
    I want to get the correct feedback and scores when I post a guess
    So that I can play on the board as game rules are followed
    """
    fixtures = ['player_alice', 'player_bob', 'bobs_game', 'bobs_first_board']

    @decorators.Scenario(base.steps)
    def test_new_game_i_am_not_the_codebreaker(self):
        """
        When I post a `guess` in a game of another user
        Then I get a 400 response saying it is not my game
        """

    @decorators.Scenario(base.steps)
    def i_guess_the_code_and_try_another_guess(self):
        """
        When I post a `guess` with code "BYGY"
        And I post a `guess` with code "RBGG"
        Then the guess "-2" is added with feedback "FFFF"
        And I get a 400 response from guess "-1" saying I already guessed the code
        And my score is "9" against "5"
        """

    @decorators.Scenario(base.steps)
    def i_post_two_guesses(self):
        """
        When I post a `guess` with code "YBYR"
        And I post a `guess` with code "PYBY"
        Then the guess "-2" is added with feedback "CCC"
        And the guess "-1" is added with feedback "FFC"
        """

    @decorators.Scenario(base.steps)
    def i_fill_the_board_and_try_another_guess(self):
        """
        When I post a `guess` with code "BYOY"
        And I post a `guess` with code "BYGY"
        Then the guess "-2" is added with feedback "FFF"
        And I get a 400 response from guess "-1" saying the board is full
        And my score is "5" against "4"
        """

    def i_post_a_guess_in_a_game_of_another_user(self, *args):
        return self.client.post('/guesses/', {'board': 2, 'code': ['R', 'G', 'Y', 'B']}),

    def i_post_a_guess_with_code_(self, *args, **kwargs):
        board = list(filter(lambda r: r.status_code == 201, self.steps.outputs['board']))[-1]

        return self.client.post('/guesses/', {
            'board': board.json()['id'], 'code': list(args[0])}),

    def the_guess__is_added_with_feedback_(self, *args):
        guess_index = int(args[0])
        expected_feedback = list(args[1]) + ['']*(settings.CODE_SIZE - len(args[1]))
        response = self.steps.outputs['guess'][guess_index]
        assert response.status_code == 201

        guess = response.json()

        assert guess['feedback'] == expected_feedback

    def i_get_a_400_response_from_guess__saying_i_already_guessed_the_code(self, *args):
        guess_index = int(args[0])
        response = self.steps.outputs['guess'][guess_index]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['You already guessed the code!']}

    def my_score_is__against_(self, *args):
        expected_breaker_score, expected_maker_score = map(int, args)
        game_id = self.steps.outputs['game'][-1].json()['id']
        game = self.client.get(f'/games/{game_id}/').json()

        assert game['breaker_score'] == expected_breaker_score
        assert game['maker_score'] == expected_maker_score

    def i_get_a_400_response_from_guess__saying_the_board_is_full(self, *args):
        guess_index = int(args[0])
        response = self.steps.outputs['guess'][guess_index]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': [
            'Board is full, you did not guess the code!']}


@mock.patch('random.choices', return_value=list('BYGY'))
class ClearBoard(NewGame, MakingGuesses, base.BaseTestCase):
    """
    As a codebreaker
    I want a clear board with a new code
    In order to start making guesses on it
    """

    @decorators.Scenario(base.steps)
    def test_clear_board_i_am_not_the_codebreaker(self, *args):
        """
        When I request a clear `board` in a game of another user
        Then I get a 400 response saying it is not my game
        """

    @decorators.Scenario(base.steps)
    def a_new_board(self, *args):
        """
        When I request a clear `board` in my game
        Then the next board is added to the game
        """

    @decorators.Scenario(base.steps)
    def an_unfinished_board(self, *args):
        """
        Given my new game
        And a new board
        And I post two guesses
        When I request a clear `board` in my game
        Then I get a 400 response with the board number and guesses left
        """

    @decorators.Scenario(base.steps)
    def test_game_is_over(self, *args):
        """
        Given an unfinished board
        And I fill the board and try another guess
        And a new board
        And I guess the code and try another guess
        When I request a clear `board` in my game
        Then I get a 400 response with the final rankings
        """

    def i_request_a_clear_board_in_a_game_of_another_user(self, *args):
        return self.client.post('/boards/', {'game': 2}),

    def i_request_a_clear_board_in_my_game(self, *args):
        return self.client.post('/boards/', {
            'game': self.steps.outputs['game'][-1].json()['id']}),

    def i_get_a_400_response_with_the_board_number_and_guesses_left(self, *args):
        response = self.steps.outputs['board'][-1]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': [
            'You have 1 guess(es) left on board 1!']}

    def i_get_a_400_response_with_the_final_rankings(self, *args):
        response = self.steps.outputs['board'][-1]
        json_response = response.json()

        assert response.status_code == 400
        assert json_response == {'non_field_errors': [
            'Game is over, all boards completed! Breaker 9 - Maker 5']}

    def the_next_board_is_added_to_the_game(self, *args):
        game_id = self.steps.outputs['game'][-1].json()['id']
        boards = self.client.get(f'/boards/?game={game_id}&ordering=number')

        assert self.steps.outputs['board'][-1].json() == boards.json()[-1]
