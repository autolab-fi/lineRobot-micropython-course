import ast
import re
import unittest
from pathlib import Path

source = Path(__file__).resolve().parents[1] / 'verifications/module_5.py'
function = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'has_line_loss_failsafe')
namespace = {'re': re}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), namespace)

class FailsafeTests(unittest.TestCase):
    def test_accepts_the_published_threshold_with_normal_spacing_variants(self):
        for code in ['if max(sensor_array) < 700:', 'if max(readings)<700:', 'if max (readings) < 700.0:']:
            self.assertTrue(namespace['has_line_loss_failsafe'](code), code)

    def test_rejects_the_stale_threshold_and_unrelated_comparison(self):
        for code in ['if max(sensor_array) < 500:', 'if max(sensor_array) < 7000:', 'if sensor_array[0] < 700:']:
            self.assertFalse(namespace['has_line_loss_failsafe'](code), code)

if __name__ == '__main__':
    unittest.main()
