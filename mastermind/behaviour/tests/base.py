from mastermind.unit_tests.base import AuthenticatedApiTestCase

from bdd_coder.tester import decorators
from bdd_coder.tester import tester

from . import steps


@decorators.Steps(steps.MAP)
class BddApiTestCase(tester.BddTestCase, AuthenticatedApiTestCase):
    def not_your_game_400(self, *args, **kwargs):
        response = (self.steps.outputs.get('board') or self.steps.outputs.get('guess'))[-1]

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['Not your game!']}
