"""Final diagnostic verdict must survive subsequent frames."""
import ast
import math
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

root = Path(__file__).resolve().parents[1]
source = root / 'verifications/module_5.py'
function = next(n for n in ast.parse(source.read_text()).body
                if isinstance(n, ast.FunctionDef) and n.name == 'concept_of_error')
clock = SimpleNamespace(now=0)
namespace = {'math': math, 're': re, 'time': SimpleNamespace(time=lambda: clock.now)}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), namespace)
reference = (root/'solutions/module_5/concept_of_error_reference.py').read_text()

class ConceptVerdictTests(unittest.TestCase):
    def replay(self, messages, distance=30, code=reference):
        clock.now = 0
        robot = SimpleNamespace(position=(0, 0), draw_info=lambda image: image, get_msg=lambda: None)
        verify = namespace['concept_of_error']
        _, state, _, _ = verify(robot, None, None, code)
        for i, message in enumerate(messages):
            clock.now = (i+1)*0.4
            robot.get_msg = lambda message=message: message
            robot.position = (distance if i >= 7 else 0, 0)
            _, state, _, _ = verify(robot, None, state, code)
        robot.get_msg = lambda: None
        clock.now = 9.5
        _, state, text, result = verify(robot, None, state, code)
        for now in (9.8, 10.1, 20):
            clock.now = now
            _, state, later_text, later = verify(robot, None, state, code)
            self.assertEqual(result, later)
            self.assertEqual(text, later_text)
        return result

    def messages(self):
        return ['Starting sweep...'] + ['Error: '+str(v) for v in (0,0,0,-.875,-.875)] + ['Sweep complete.', 'Starting sweep...'] + ['Error: '+str(v) for v in (0,-.5,-.75,-1,-1)] + ['Sweep complete.']

    def test_measured_success_stays_successful(self):
        self.assertTrue(self.replay(self.messages(),26.6)['success'])

    def test_no_messages_stays_failed(self):
        self.assertFalse(self.replay([])['success'])

    def test_insufficient_messages_stays_failed(self):
        self.assertFalse(self.replay(['Starting sweep...', 'Error: 0'])['success'])

    def test_wrong_distance_stays_failed(self):
        self.assertFalse(self.replay(self.messages(),10)['success'])

    def test_invalid_code_stays_failed(self):
        self.assertFalse(self.replay(self.messages(),30,'pass')['success'])
