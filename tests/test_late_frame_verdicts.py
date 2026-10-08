"""An expired unsuccessful attempt must not pass on a later camera frame."""
import ast
import math
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

TASKS = {
    'module_4.py': ('python_lists', 'telemetry', 'color_sensor_basics', 'color_classification'),
    'module_11.py': ('perimeter', 'adaptive_racing'),
}

class LateFrameVerdicts(unittest.TestCase):
    def test_repeated_frames_preserve_failure_and_score(self):
        for module, tasks in TASKS.items():
            source = Path(__file__).resolve().parents[1] / 'verifications' / module
            functions = [n for n in ast.parse(source.read_text()).body
                         if isinstance(n, ast.FunctionDef) and n.name in tasks]
            clock = SimpleNamespace(now=0.0)
            namespace = {
                'ast': ast, 'math': math, 'os': os, 're': re, '__file__': str(source),
                'time': SimpleNamespace(time=lambda: clock.now),
                'cv2': SimpleNamespace(imread=lambda *args: None, IMREAD_UNCHANGED=-1),
            }
            exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), namespace)
            for task in tasks:
                with self.subTest(task=task):
                    clock.now = 0
                    robot = SimpleNamespace(
                        draw_info=lambda frame: frame, get_msg=lambda: None,
                        get_info=lambda: {'position': None, 'position_px': None},
                        position=None, position_px=None,
                    )
                    verify = namespace[task]
                    _, state, _, _ = verify(robot, None, None, 'pass')
                    clock.now = state['end_time'] + .1
                    _, state, text, result = verify(robot, None, state, 'pass')
                    self.assertFalse(result['success'])
                    expected = result.copy()
                    result['success'] = True  # Caller mutation must not corrupt stored verdict.
                    for _ in range(3):
                        clock.now += .2
                        _, state, later_text, later = verify(robot, None, state, 'pass')
                        self.assertEqual(later, expected)
                        self.assertEqual(later_text, text)
