"""Replay real sensor logs and reject labels/errors masquerading as readings."""
import ast
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

source = Path(__file__).resolve().parents[1] / 'verifications/module_3.py'
function = next(n for n in ast.parse(source.read_text()).body
                if isinstance(n, ast.FunctionDef) and n.name == 'intro_to_octoliner')
clock = SimpleNamespace(now=0.0)
namespace = {'ast': ast, 're': re, 'time': SimpleNamespace(time=lambda: clock.now),
             'cv2': SimpleNamespace(putText=lambda *a: None, FONT_HERSHEY_SIMPLEX=0)}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), namespace)
verify = namespace['intro_to_octoliner']

class SensorVerdictTests(unittest.TestCase):
    def replay(self, messages, code='print(sensor.analog_read(3))\nprint(sensor.analog_read(4))'):
        clock.now = 0
        robot = SimpleNamespace(draw_info=lambda image: image, get_msg=lambda: None)
        _, state, _, _ = verify(robot, None, None, code)
        for message in messages:
            robot.get_msg = lambda: message
            _, state, _, _ = verify(robot, None, state, code)
        clock.now = 11
        robot.get_msg = lambda: None
        return state['data'], verify(robot, None, state, code)[3]

    def test_real_log_21836_values_not_channel_numbers(self):
        data, result = self.replay(['Sensor 3 : 52', 'Sensor 4 : 55', 'Sensor 3 : 53', 'Sensor 4 : 57'])
        self.assertTrue(result['success'])
        self.assertEqual((data['sensor_3'], data['sensor_4']), (53, 57))
        self.assertIn('S3=53, S4=57', result['description'])

    def test_channel_order_and_repeated_readings(self):
        data, _ = self.replay(['Sensor 4: 700', 'Sensor 4: 701', 'Sensor 3: 0'])
        self.assertEqual((data['sensor_3'], data['sensor_4']), (0, 701))

    def test_bare_value_for_single_channel(self):
        for channel in (3, 4):
            data, result = self.replay(['1023'], f'print(sensor.analog_read( {channel} ))')
            self.assertTrue(result['success'])
            self.assertEqual(data[f'sensor_{channel}'], 1023)

    def test_diagnostics_invalid_values_and_labels_are_not_readings(self):
        for message in ['Sensor 3', 'OSError: [Errno 19] ENODEV', 'MPY: soft reboot',
                        'I2C scan: [42]', 'Sensor 3: -1', 'Sensor 3: 1024',
                        'Sensor 3: 52.5', 'Sensor 4: nan', 'Traceback line 53']:
            with self.subTest(message=message):
                _, result = self.replay([message])
                self.assertFalse(result['success'])

    def test_multiline_and_label_variants(self):
        data, result = self.replay(['s4=800\nSensor 3 : 53'])
        self.assertTrue(result['success'])
        self.assertEqual((data['sensor_3'], data['sensor_4']), (53, 800))

    def test_comment_or_string_is_not_a_read_call(self):
        for code in ['# sensor.analog_read(3)', 'print("analog_read(3)")']:
            _, result = self.replay(['Sensor 3: 53'], code)
            self.assertFalse(result['success'])

    def test_wrong_channel_and_ambiguous_bare_number(self):
        _, result = self.replay(['Sensor 4: 53'], 'print(sensor.analog_read(3))')
        self.assertFalse(result['success'])
        _, result = self.replay(['53'])
        self.assertFalse(result['success'])

if __name__ == '__main__':
    unittest.main()
