import os

from bdd_coder.tester import decorators
from bdd_coder.tester import tester

from mastermind.unit_tests.base import AuthenticatedApiTestCase

from . import aliases

steps = decorators.Steps(aliases.MAP, os.path.dirname(os.path.abspath(__file__)))


@steps
class BddTester(tester.BddTester):
    pass


class BaseTestCase(AuthenticatedApiTestCase, tester.BaseTestCase):

    def not_your_game_400(self):
        response = (self.steps.outputs.get('board') or self.steps.outputs.get('guess'))[-1]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['Not your game!']}
