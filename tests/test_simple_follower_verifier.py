"""Replay the measured line route and verify that a final verdict stays final."""
import ast
import contextlib
import io
import math
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

source = Path(__file__).resolve().parents[1] / 'verifications/module_3.py'
functions = [n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef)
             and n.name in ('simple_line_follower',)]
clock = SimpleNamespace(now=0.0)
namespace = {'math': math, 'os': os, 're': re, '__file__': str(source),
             'time': SimpleNamespace(time=lambda: clock.now),
             'cv2': SimpleNamespace(imread=lambda path: None)}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), namespace)
verify = namespace['simple_line_follower']
reference = (source.parents[1] / 'solutions/module_3/simple_line_follower_reference.py').read_text()

class SimpleFollowerTests(unittest.TestCase):
    def replay(self, positions, code=reference):
        clock.now = 0
        robot = SimpleNamespace(position=positions[0], position_px=None,
                                draw_info=lambda image: image, get_msg=lambda: None)
        with contextlib.redirect_stdout(io.StringIO()):
            _, state, _, _ = verify(robot, None, None, code)
        for index, pos in enumerate(positions[1:], 1):
            clock.now = index * 2
            robot.position = pos
            _, state, _, _ = verify(robot, None, state, code)
        if not state['data']['completed']:
            clock.now = 89.5
        _, state, text, result = verify(robot, None, state, code)
        clock.now += 1
        _, state, later_text, later = verify(robot, None, state, code)
        self.assertEqual(result, later)
        self.assertEqual(text, later_text)
        return state, result

    def test_complete_route_finishes_even_before_ten_seconds(self):
        state, result = self.replay([(104,40),(104,52),(103,64)])
        self.assertTrue(result['success'])
        self.assertEqual(state['end_time'],4)

    def test_one_checkpoint_is_not_complete(self):
        _, result = self.replay([(104,40),(104,52)])
        self.assertFalse(result['success'])
        self.assertEqual(result['score'],50)

    def test_wrong_order_fails(self):
        _, result = self.replay([(104,40),(103,64),(104,52)])
        self.assertFalse(result['success'])

    def test_empty_code_cannot_pass_by_motion(self):
        _, result = self.replay([(104,40),(104,52),(103,64)],'pass')
        self.assertFalse(result['success'])

if __name__ == '__main__':
    unittest.main()
