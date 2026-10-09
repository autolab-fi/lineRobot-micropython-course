"""A safe slower lap must finish before the documented 90-second deadline."""
import ast,math,os,re
from pathlib import Path
from types import SimpleNamespace
import unittest
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'verifications/module_5.py'
FUNCTIONS=[n for n in ast.parse(SOURCE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ('proportional_control','has_line_loss_failsafe')]
CODE=(ROOT/'solutions/module_5/proportional_control_reference.py').read_text()
class PControllerTimingTests(unittest.TestCase):
 def setup_replay(self):
  clock=SimpleNamespace(now=0)
  ns={'math':math,'os':os,'re':re,'__file__':str(SOURCE),'time':SimpleNamespace(time=lambda:clock.now),'cv2':SimpleNamespace(imread=lambda *args:None)}
  exec(compile(ast.Module(body=FUNCTIONS,type_ignores=[]),str(SOURCE),'exec'),ns)
  robot=SimpleNamespace(position=(40,30),position_px=None,draw_info=lambda frame:frame,get_msg=lambda:None)
  verify=ns['proportional_control'];_,state,_,_=verify(robot,None,None,CODE)
  return clock,robot,verify,state
 def test_lap_completed_at_seventy_seconds_is_accepted(self):
  clock,robot,verify,state=self.setup_replay()
  for timestamp,point in [(25,(105,60)),(40,(60,90)),(60.1,(40,30)),(70,(80,30))]:
   clock.now=timestamp;robot.position=point;_,state,_,_=verify(robot,None,state,CODE)
   if timestamp==60.1:self.assertIsNone(state['data'].get('final_result'))
  clock.now=90.1;_,state,_,result=verify(robot,None,state,CODE)
  self.assertTrue(result['success'])
 def test_late_checkpoint_cannot_change_failed_verdict(self):
  clock,robot,verify,state=self.setup_replay()
  for timestamp,point in [(25,(105,60)),(40,(60,90))]:
   clock.now=timestamp;robot.position=point;_,state,_,_=verify(robot,None,state,CODE)
  clock.now=90.1;_,state,text,result=verify(robot,None,state,CODE)
  self.assertFalse(result['success']);expected=result.copy();result['success']=True
  clock.now=95;robot.position=(80,30);_,state,later_text,later=verify(robot,None,state,CODE)
  self.assertEqual(expected,later);self.assertEqual(text,later_text)
if __name__=='__main__':unittest.main()
