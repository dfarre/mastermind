import os

from bdd_coder.tester import decorators
from bdd_coder.tester import tester

from mastermind.unit_tests.base import AuthenticatedDjangoTestCase

from . import aliases

steps = decorators.Steps(aliases.MAP, logs_path=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'bdd_runs.log'))
scenario = decorators.Scenario(steps)


@steps
class BddTester(tester.BddTester):
    pass


class BaseTestCase(AuthenticatedDjangoTestCase, tester.BaseTestCase):
    def not_your_game_400(self):
        response = (self.steps.outputs.get('board') or self.steps.outputs.get('guess'))[-1]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['Not your game!']}
