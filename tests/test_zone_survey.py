"""Execute both references with every zone combination; replay the lab message checks."""
import ast
import contextlib
import io
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'verifications/module_3.py'
names = {'_record_zone_report', '_zone_reports_valid', 'arrays_and_elif', 'led_feedback'}
functions = [n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in names]
clock = SimpleNamespace(now=0)
namespace = {'ast': ast, 'time': SimpleNamespace(time=lambda: clock.now)}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), namespace)

class SurveyTests(unittest.TestCase):
    def execute(self, task, masks):
        readings = []
        for mask in masks:
            values = [100] * 8
            for i, channel in enumerate((6, 3, 1)):
                values[channel] = 900 if mask & (1 << i) else 800
            readings.append(values)
        frames = iter(readings)
        pulses, moves = [], []
        class Pin:
            OUT = 1
            def __init__(self, *args): pass
            def on(self): pulses.append('on')
            def off(self): pulses.append('off')
        sensor = SimpleNamespace(begin=lambda _: None, set_sensitivity=lambda _: None,
                                 analog_read_all=lambda: next(frames))
        mocks = {'machine': SimpleNamespace(Pin=Pin, I2C=lambda **kwargs: None),
                 'time': SimpleNamespace(sleep=lambda _: None),
                 'octoliner': SimpleNamespace(Octoliner=lambda: sensor),
                 'lineRobot': SimpleNamespace(Robot=lambda: SimpleNamespace(move_forward_distance=moves.append))}
        code = (ROOT / f'solutions/module_3/{task}_reference.py').read_text()
        output = io.StringIO()
        with patch.dict(sys.modules, mocks), contextlib.redirect_stdout(output):
            exec(code, {})
        self.assertEqual(moves, [5] * 5)
        self.assertEqual(pulses, ['on', 'off'] * sum(bool(m) for m in masks) if task == 'led_feedback' else [])
        return code, output.getvalue().splitlines()

    def verify(self, task, code, messages):
        pending = iter(messages)
        robot = SimpleNamespace(draw_info=lambda image: image, get_msg=lambda: next(pending, None))
        clock.now = 0
        state = None
        for _ in range(len(messages) + 1):
            _, state, _, _ = namespace[task](robot, None, state, code)
        clock.now = 31
        return namespace[task](robot, None, state, code)[3]['success']

    def test_references_cover_all_zone_combinations(self):
        for task in ('arrays_and_elif', 'led_feedback'):
            for masks in ([0, 1, 2, 3, 4], [4, 5, 6, 7, 0]):
                with self.subTest(task=task, masks=masks):
                    code, messages = self.execute(task, masks)
                    self.assertTrue(self.verify(task, code, messages))
                    self.assertFalse(self.verify(task, code, [m for m in messages if not m.startswith('Left:')]))
                    bad = list(messages)
                    bad[0] = 'Line in multiple zones' if bad[0] == 'No line' else 'No line'
                    self.assertFalse(self.verify(task, code, bad))

    def test_mqtt_concatenation_and_packet_fragmentation(self):
        for task in ('arrays_and_elif', 'led_feedback'):
            code, messages = self.execute(task, [0, 1, 3, 7, 0])
            stream = ''.join(messages)
            self.assertTrue(self.verify(task, code, [stream]))
            self.assertTrue(self.verify(task, code, [stream[i:i+7] for i in range(0, len(stream), 7)]))
            self.assertFalse(self.verify(task, code, [stream.replace('Left: True', 'Left: False', 1)]))
