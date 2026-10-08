import ast,math
from pathlib import Path
from types import SimpleNamespace
import unittest
P=Path(__file__).resolve().parents[1]/'verifications/module_2.py'
FN=next(n for n in ast.parse(P.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='defining_functions')
GOOD='def turn():\n    rover.run_motors_speed(28,-38)\n    rover.stop()\nturn()'
class FunctionVerifierTests(unittest.TestCase):
 def verdict(self,code=GOOD,start=0,end=180,stable=True):
  clock=SimpleNamespace(now=0);angle=start
  ns={'ast':ast,'time':SimpleNamespace(time=lambda:clock.now)}
  exec(compile(ast.Module(body=[FN],type_ignores=[]),str(P),'exec'),ns)
  robot=SimpleNamespace(draw_info=lambda x:x,compute_angle_x=lambda:angle)
  _,td,_,_=ns['defining_functions'](robot,None,None,code)
  clock.now=8;angle=end if stable else start
  _,td,_,_=ns['defining_functions'](robot,None,td,code)
  clock.now=9.5;angle=end
  _,td,_,result=ns['defining_functions'](robot,None,td,code)
  clock.now=12;angle=start
  self.assertEqual(result,ns['defining_functions'](robot,None,td,code)[3])
  return result['success']
 def test_defined_called_function_and_wraparound(self):
  self.assertTrue(self.verdict())
  self.assertTrue(self.verdict(start=179,end=1))
 def test_missing_or_uncalled_function_and_banned_motion(self):
  for code in ['rover.run_motors_speed(28,-38)\nrover.stop()',GOOD.replace('\nturn()',''),GOOD.replace('run_motors_speed(28,-38)','turn_right_angle(180)')]:self.assertFalse(self.verdict(code))
 def test_wrong_or_unsettled_heading(self):
  self.assertFalse(self.verdict(end=40))
  self.assertFalse(self.verdict(stable=False))
