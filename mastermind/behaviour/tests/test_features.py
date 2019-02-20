import unittest.mock as mock

from bdd_coder.tester import decorators

from django.conf import settings

from . import base


class NewGame(base.BddApiTestCase):
    """
    As a codebreaker
    I want to start a new Mastermind game of B boards of G guesses
    In order to play
    """

    @decorators.scenario
    def A_odd_boards(self):
        """
        When I request a new `game` of "9" boards of "12" guesses
        Then I get a 400 response saying it must be even
        """

    @decorators.scenario
    def start_game(self):
        """
        When I request a new `game` of "2" boards of "3" guesses
        Then a game of "2" boards of "3" guesses and me as the codebreaker is created
        """

    def i_request_a_new_game_of__boards_of__guesses(self, *args, **kwargs):
        return self.client.post('/games/', {
            'last_board': int(args[0]), 'board_size': int(args[1])}),

    def i_get_a_400_response_saying_it_must_be_even(self, *args, **kwargs):
        response = self.steps.outputs['game'][-1]

        assert response.status_code == 400
        assert response.json() == {'last_board': ['Number of boards to play must be even.']}

    def a_game_of__boards_of__guesses_and_me_as_the_codebreaker_is_created(
            self, *args, **kwargs):
        response = self.steps.outputs['game'][-1]
        game = {**response.json()}

        assert response.status_code == 201

        game.pop('id')

        assert game == {
            'last_board': int(args[0]), 'board_size': int(args[1]),
            'codebreaker': self.user.id, 'breaker_score': 0, 'maker_score': 0}


class MakingGuesses(NewGame):
    """
    As a codebreaker
    I want to get the correct feedback and scores when I post a guess
    So that I can play on the board as game rules are followed
    """
    fixtures = ['player_alice', 'player_bob', 'bobs_game', 'bobs_first_board']

    @decorators.scenario
    def B_i_am_not_the_codebreaker(self):
        """
        When I post a `guess` in a game of another user
        Then I get a 400 response saying it is not my game
        """

    @decorators.scenario
    def i_guess_the_code_and_try_another_guess(self):
        """
        Given I post a `guess` with code "BYGY"
        And I post a `guess` with code "RBGG"
        Then the guess "1" is added with feedback "FFFF"
        And I get a 400 response from guess "2" saying I already guessed the code
        And my score is "4" against "1"
        """

    @decorators.scenario
    def i_post_two_guesses(self):
        """
        When I post a `guess` with code "YBYR"
        And I post a `guess` with code "PYBY"
        Then the guess "-2" is added with feedback "CCC"
        And the guess "-1" is added with feedback "FFC"
        """

    @decorators.scenario
    def i_fill_the_board_and_try_another_guess(self):
        """
        When I post a `guess` with code "BYOY"
        And I post a `guess` with code "BYGY"
        Then the guess "-2" is added with feedback "FFF"
        And I get a 400 response from guess "-1" saying the board is full
        And my score is "5" against "4"
        """

    def i_post_a_guess_in_a_game_of_another_user(self, *args, **kwargs):
        return self.client.post('/guesses/', {'board': 2, 'code': ['R', 'G', 'Y', 'B']}),

    def i_post_a_guess_with_code_(self, *args, **kwargs):
        return self.client.post('/guesses/', {
            'board': self.steps.outputs['board'][-1].json()['id'], 'code': list(args[0])}),

    def the_guess__is_added_with_feedback_(self, *args, **kwargs):
        guess_index = int(args[0])
        expected_feedback = list(args[1]) + ['']*(settings.CODE_SIZE - len(args[1]))
        response = self.steps.outputs['guess'][guess_index]
        assert response.status_code == 201

        guess = response.json()

        assert guess['feedback'] == expected_feedback

    def i_get_a_400_response_from_guess__saying_i_already_guessed_the_code(
            self, *args, **kwargs):
        expected_number = int(args[1])
        response = self.steps.outputs['guess'][expected_number - 1]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['You already guessed the code!']}

    def my_score_is__against_(self, *args, **kwargs):
        expected_breaker_score, expected_maker_score = args
        game_id = self.steps.outputs['game'][-1].json()['id']
        game = self.client.get(f'/games/{game_id}')

        assert game['breaker_score'] == expected_breaker_score
        assert game['maker_score'] == expected_maker_score

    def i_get_a_400_response_from_guess__saying_the_board_is_full(self, *args, **kwargs):
        guess_index = int(args[0])
        response = self.steps.outputs['guess'][guess_index]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': [
            'Board is full, you did not guess the code!']}


@mock.patch('random.choices', return_value=list("BYGY"))
class ClearBoard(MakingGuesses):
    """
    As a codebreaker
    I want a clear board with a new code
    In order to start making guesses on it
    """

    @decorators.scenario
    def D_i_am_not_the_codebreaker(self):
        """
        When I request a clear `board` in a game of another user
        Then I get a 400 response saying it is not my game
        """

    @decorators.scenario
    def start_board(self):
        """
        When I request a clear `board` in my game
        Then the next board is added to the game
        """

    @decorators.scenario
    def unfinished_board(self):
        """
        Given there is an unfinished board
        When I request a clear `board` in my game
        Then I get a 400 response with the board number and guesses left
        """

    @decorators.scenario
    def C_game_is_over(self):
        """
        Given all boards are over
        When I request a clear `board` in my game
        Then I get a 400 response with the final rankings
        """

    def test_game(self, random_choices_mock):
        self.A_odd_boards()
        self.B_i_am_not_the_codebreaker()
        self.C_game_is_over()
        self.D_i_am_not_the_codebreaker()

    def i_request_a_clear_board_in_a_game_of_another_user(self, *args, **kwargs):
        return self.client.post('/boards/', {'game': 2}),

    def i_request_a_clear_board_in_my_game(self, *args, **kwargs):
        return self.client.post('/boards/', {
            'game': self.steps.outputs['game'][-1].json()['id']}),

    def there_is_an_unfinished_board(self, *args, **kwargs):
        self.start_game()
        self.start_board()
        self.i_post_two_guesses()

    def i_get_a_400_response_with_the_board_number_and_guesses_left(self, *args, **kwargs):
        response = self.steps.outputs['board'][-1]
        json_response = response.json()

        assert response.status_code == 400
        assert json_response == {'non_field_errors': ['You have  guesses left on board !']}

    def all_boards_are_over(self, *args, **kwargs):
        self.there_is_an_unfinished_board()
        self.i_fill_the_board_and_try_another_guess()
        self.start_board()
        self.i_guess_the_code_and_try_another_guess()

    def i_get_a_400_response_with_the_final_rankings(self, *args, **kwargs):
        response = self.steps.outputs['board'][-1]
        json_response = response.json()

        assert response.status_code == 400
        assert json_response == {'non_field_errors': [
            'Game is over, all boards completed! Breaker 5 - Maker 4']}

    def the_next_board_is_added_to_the_game(self, *args, **kwargs):
        game_id = self.steps.outputs['game'][-1].json()['id']
        boards = self.client.get(f'/boards/?game={game_id}&ordering=number')

        assert self.steps.outputs['board'][-1].json() == boards.json()[-1]
