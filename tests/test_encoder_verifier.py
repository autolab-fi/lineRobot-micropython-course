import ast,math,re
from pathlib import Path
from types import SimpleNamespace
import unittest
P=Path(__file__).resolve().parents[1]/'verifications/module_2.py'
FN=next(n for n in ast.parse(P.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='encoder_theory')
CODE='import math\nrobot.reset_left_encoder()\nrobot.reset_right_encoder()\nprint(math.pi)'
class EncoderVerifierTests(unittest.TestCase):
 def verdict(self,left=335,right=340,distance=None,displacement=20,split=False):
  clock=SimpleNamespace(now=0);pending=[]
  ns={'math':math,'re':re,'time':SimpleNamespace(time=lambda:clock.now)}
  exec(compile(ast.Module(body=[FN],type_ignores=[]),str(P),'exec'),ns)
  robot=SimpleNamespace(position=(30,50),draw_info=lambda x:x,delta_points=lambda a,b:math.dist(a,b),get_msg=lambda:pending.pop(0) if pending else None)
  _,td,_,_=ns['encoder_theory'](robot,None,None,CODE)
  distance=left/360*2*math.pi*3.21 if distance is None else distance
  text=f'Encoder degrees left: {left}Distance in cm: {distance}'
  if right is not None:text+=f'Encoder degrees right: {right}'
  pending.extend([text[:15],text[15:]] if split else [text])
  clock.now=19.5;robot.position=(30+displacement,50)
  return ns['encoder_theory'](robot,None,td,CODE)[3]['success']
 def test_merged_and_split_messages_preserve_values(self):
  self.assertTrue(self.verdict())
  self.assertTrue(self.verdict(split=True))
 def test_both_encoders_and_formula_required(self):
  self.assertFalse(self.verdict(right=None))
  self.assertFalse(self.verdict(right=400))
  self.assertFalse(self.verdict(left=310,distance=20.8))
 def test_printed_values_without_movement_fail(self):
  self.assertFalse(self.verdict(displacement=0))
