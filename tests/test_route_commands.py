"""Camera tolerance must not accept incorrect distance/turn programs."""
import ast
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'verifications/module_11.py'
HELPER = next(n for n in ast.parse(SOURCE.read_text()).body
              if isinstance(n, ast.FunctionDef) and n.name == '_student_route_matches')
namespace = {'ast': ast, 'math': math}
exec(compile(ast.Module(body=[HELPER], type_ignores=[]), str(SOURCE), 'exec'), namespace)
matches = namespace['_student_route_matches']
NAV = [('move', 20), ('turn', -45), ('move', 40), ('turn', 45),
       ('move', 20), ('turn', 90), ('move', 40)]
SQUARE = [('move', 30), ('turn', 90)] * 4


class RouteCommands(unittest.TestCase):
    def test_canonical_routes(self):
        for task, expected in [('navigation', NAV), ('perimeter', SQUARE)]:
            self.assertTrue(matches((ROOT / f'solutions/module_11/{task}_reference.py').read_text(), expected))

    def test_renaming_arithmetic_loops_and_helpers(self):
        code = '''from lineRobot import Robot
rover = Robot()
side = 60 / 2
def leg(distance):
    rover.move_forward_distance(distance)
    rover.turn_right()
for step in range(2 + 2):
    leg(side)
rover.stop()
'''
        self.assertTrue(matches(code, SQUARE))

    def test_wrong_route_commands_fail(self):
        reference = (ROOT / 'solutions/module_11/navigation_reference.py').read_text()
        for code in [reference.replace('first_distance = 20', 'first_distance = 10'),
                     reference.replace('small_angle = 45', 'small_angle = 90'),
                     reference.replace('turn_left_angle', 'turn_right_angle'),
                     reference + '\nrobot.move_forward_distance(10)']:
            with self.subTest(code=code):
                self.assertFalse(matches(code, NAV))

    def test_distance_without_turns_is_not_a_square(self):
        self.assertFalse(matches('for i in range(4):\n    robot.move_forward_distance(30)', SQUARE))

    def test_unbounded_or_dynamic_routes_fail_safely(self):
        for code in ['for i in range(1000000):\n    robot.turn_right()',
                     'def f():\n    f()\nf()', 'while True:\n    robot.turn_right()',
                     'robot.move_forward_distance(float("inf"))',
                     'robot.move_forward_distance(30/0)', 'robot.move_forward_distance(unknown)']:
            self.assertFalse(matches(code, SQUARE))


if __name__ == '__main__':
    unittest.main()
