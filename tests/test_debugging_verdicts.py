"""Failures must remain failures on every frame sent to the worker."""
import ast
import math
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

source = Path(__file__).resolve().parents[1] / 'verifications/module_6.py'
clock = SimpleNamespace(now=0.0)
functions = [n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef)
             and n.name in ('art_of_debugging', 'hardware_safety_net', 'code_clinic')]
namespace = {'ast': ast, 'math': math, 'os': os, 're': re, '__file__': str(source),
             'time': SimpleNamespace(time=lambda: clock.now),
             'cv2': SimpleNamespace(imread=lambda *args: None, IMREAD_UNCHANGED=-1)}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), namespace)

class DebuggingVerdicts(unittest.TestCase):
    def test_empty_attempt_cannot_become_success_on_later_frame(self):
        for name in ('art_of_debugging', 'hardware_safety_net', 'code_clinic'):
            with self.subTest(task=name):
                clock.now=0
                robot=SimpleNamespace(draw_info=lambda frame: frame, get_msg=lambda: None,
                                      position=None, position_px=None)
                verify=namespace[name]
                _, state, _, _=verify(robot, None, None, 'pass')
                clock.now=state['end_time'] + .1
                _, state, text, verdict=verify(robot, None, state, 'pass')
                self.assertFalse(verdict['success'])
                clock.now+=1
                _, _, later_text, later=verify(robot, None, state, 'pass')
                self.assertEqual(later,verdict)
                self.assertEqual(later_text,text)
