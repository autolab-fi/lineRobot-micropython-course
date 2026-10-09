"""Replay the measured relay route and verify that a final verdict stays final."""
import ast
import contextlib
import io
import math
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

source = Path(__file__).resolve().parents[1] / 'verifications/module_5.py'
functions = [n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef)
             and n.name in ('has_line_loss_failsafe', 'upgraded_relay_controller')]
clock = SimpleNamespace(now=0.0)
namespace = {'math': math, 'os': os, 're': re, '__file__': str(source),
             'time': SimpleNamespace(time=lambda: clock.now),
             'cv2': SimpleNamespace(imread=lambda path: None)}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), namespace)
verify = namespace['upgraded_relay_controller']
reference = (source.parents[1] / 'solutions/module_5/upgraded_relay_controller_reference.py').read_text()

class RelayVerdictTests(unittest.TestCase):
    def replay(self, positions, code=reference):
        clock.now = 0
        robot = SimpleNamespace(position=positions[0], position_px=None,
                                draw_info=lambda image: image, get_msg=lambda: None)
        with contextlib.redirect_stdout(io.StringIO()):
            _, state, _, _ = verify(robot, None, None, code)
        for index, position in enumerate(positions[1:], 1):
            clock.now = index * 10
            robot.position = position
            _, state, _, _ = verify(robot, None, state, code)
        clock.now = 89.5
        _, state, text, result = verify(robot, None, state, code)
        clock.now = 90.1
        _, _, later_text, later = verify(robot, None, state, code)
        self.assertEqual(later, result)
        self.assertEqual(later_text, text)
        return state['data'], result

    def test_hamk_route_reaches_all_markers(self):
        data, result = self.replay([(40, 30), (105, 60), (60, 90), (80, 30)])
        self.assertEqual(len(data['checkpoints_hit']), 3)
        self.assertTrue(result['success'])
        self.assertIn('Checkpoints: 3/3', result['description'])

    def test_large_motion_without_checkpoints_fails(self):
        _, result = self.replay([(40, 30), (90, 30)])
        self.assertFalse(result['success'])

    def test_incomplete_route_fails(self):
        _, result = self.replay([(40, 30), (105, 60), (60, 90)])
        self.assertFalse(result['success'])

    def test_wrong_order_fails(self):
        _, result = self.replay([(40, 30), (80, 30), (60, 90), (105, 60)])
        self.assertFalse(result['success'])

    def test_stationary_reference_fails_and_stays_failed(self):
        _, result = self.replay([(40, 30), (40.1, 30)])
        self.assertFalse(result['success'])
        self.assertEqual(result['score'], 0)

    def test_motion_without_required_code_fails(self):
        _, result = self.replay([(40, 30), (100, 60)], 'print("done")')
        self.assertFalse(result['success'])

if __name__ == '__main__':
    unittest.main()
