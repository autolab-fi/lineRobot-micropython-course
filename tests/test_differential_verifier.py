import ast, contextlib, io, math, os
from pathlib import Path
from types import SimpleNamespace
import unittest
P=Path(__file__).resolve().parents[1]/'verifications/module_2.py'
FN=next(n for n in ast.parse(P.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='differential_drive')
CODE='rover.run_motor_left(200)\nrover.run_motor_right(200)\nrover.stop()'
class DifferentialVerifierTests(unittest.TestCase):
 def run_drive(self,samples,code=CODE):
  clock=SimpleNamespace(now=0);heading=0
  ns={'ast':ast,'os':os,'__file__':str(P),'time':SimpleNamespace(time=lambda:clock.now)}
  exec(compile(ast.Module(body=[FN],type_ignores=[]),str(P),'exec'),ns)
  robot=SimpleNamespace(position=(30,50),position_px=None,draw_info=lambda x:x,compute_angle_x=lambda:heading,delta_points=math.dist)
  with contextlib.redirect_stdout(io.StringIO()):_,td,_,_=ns['differential_drive'](robot,None,None,code)
  td['data']['direction_0']=0
  for t,x,h in samples:
   clock.now=t;robot.position=(x,50) if x is not None else None;heading=h
   _,td,_,result=ns['differential_drive'](robot,None,td,code)
  clock.now=12
  self.assertEqual(result,ns['differential_drive'](robot,None,td,code)[3])
  return result['success']
 def test_three_second_pulse_includes_adjacent_still_frames(self):
  samples=[(0,30,0),(0.3,30,0),(0.6,32,0),(1,35,0),(2,41,0),(3,47,0),(3.3,49,0),(3.6,49,0),(4.3,49,0),(9.5,49,0)]
  self.assertTrue(self.run_drive(samples))
 def test_short_pulse_and_no_motion_fail(self):
  self.assertFalse(self.run_drive([(0,30,0),(1,34,0),(1.3,34,0),(2,34,0),(9.5,34,0)]))
  self.assertFalse(self.run_drive([(0,30,0),(9.5,30,0)]))
 def test_drift_and_missing_stop_fail(self):
  samples=[(0,30,0),(1,35,15),(3,45,15),(3.3,45,15),(4,45,15),(9.5,45,15)]
  self.assertFalse(self.run_drive(samples))
  self.assertFalse(self.run_drive(samples,code=CODE.replace('rover.stop()','')))
