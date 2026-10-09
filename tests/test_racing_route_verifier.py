"""The HAMK race needs its route, not just 30 cm of arbitrary motion."""
import ast,math,re
from pathlib import Path
from types import SimpleNamespace
import unittest
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'verifications/module_11.py'
FN=next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='adaptive_racing')
REFERENCE=(ROOT/'solutions/module_11/adaptive_racing_reference.py').read_text()

class RacingRouteTests(unittest.TestCase):
 def replay(self,points,code=REFERENCE):
  clock=SimpleNamespace(now=0)
  ns={'ast':ast,'math':math,'re':re,'time':SimpleNamespace(time=lambda:clock.now)}
  exec(compile(ast.Module(body=[FN],type_ignores=[]),str(SOURCE),'exec'),ns)
  robot=SimpleNamespace(position=(40,30),draw_info=lambda frame:frame)
  robot.get_info=lambda:{'position':robot.position}
  verify=ns['adaptive_racing'];_,state,_,_=verify(robot,None,None,code)
  for index,point in enumerate(points):
   clock.now=index+1;robot.position=point
   _,state,_,_=verify(robot,None,state,code)
  clock.now=60.1
  _,state,text,result=verify(robot,None,state,code)
  expected=result.copy();result['success']=not result['success'];clock.now=100
  _,_,later_text,later=verify(robot,None,state,code)
  self.assertEqual(later,expected);self.assertEqual(later_text,text)
  return expected
 def test_full_route_passes(self):self.assertTrue(self.replay([(105,60),(60,90),(80,30)])['success'])
 def test_straight_distance_alone_fails(self):self.assertFalse(self.replay([(80,30)])['success'])
 def test_skipped_first_checkpoint_fails(self):self.assertFalse(self.replay([(60,90),(80,30)])['success'])
 def test_partial_route_fails(self):
  result=self.replay([(105,60)]);self.assertFalse(result['success']);self.assertEqual(result['score'],33)
 def test_motion_cannot_pass_invalid_code(self):self.assertFalse(self.replay([(105,60),(60,90),(80,30)],'pass')['success'])
 def test_filter_sleep_does_not_hide_unfixed_five_second_delay(self):
  code=REFERENCE.rsplit('time.sleep(0.01)',1)[0]+'time.sleep(5)\n'
  self.assertIn('time.sleep(0.01)',code)
  self.assertFalse(self.replay([(105,60),(60,90),(80,30)],code)['success'])

if __name__=='__main__':unittest.main()
