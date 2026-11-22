import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

P = Path(__file__).resolve().parents[1] / 'verifications/module_1.py'
FN = next(n for n in ast.parse(P.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'directional_movement')

class VariableDistanceFeedbackTests(unittest.TestCase):
    def test_feedback_uses_task_specific_distances(self):
        clock = SimpleNamespace(now=0)
        ns = {'time': SimpleNamespace(time=lambda: clock.now)}
        exec(compile(ast.Module(body=[FN], type_ignores=[]), str(P), 'exec'), ns)
        robot = SimpleNamespace(draw_info=lambda image: image, get_info=lambda: {'position': None})
        for forward, backward in [(15, 20.5), (20, 35)]:
            td = {'end_time': 20, 'prev_robot_center': None, 'goal': {'forward': forward, 'backward': backward}}
            _, td, _, _ = ns['directional_movement'](robot, None, td)
            td['goal']['forward'] -= 2
            td['goal']['backward'] -= 4
            clock.now = 19
            result = ns['directional_movement'](robot, None, td)[3]
            self.assertIn('2.0 cm forward, 4.0 cm backward', result['description'])
            clock.now = 0
