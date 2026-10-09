"""Replay measured HAMK RGB samples; all-floor output must not pass."""
import ast
import contextlib
import io
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'verifications/module_4.py'
NAMES={'_has_scan_step','_rgb_scan_zone','_scan_label_plausible','color_sensor_basics','color_classification'}
FUNCTIONS=[n for n in ast.parse(SOURCE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in NAMES]
SAMPLES=[(89,113,48),(108,85,60),(107,85,60),(107,86,60),(106,85,59),(184,47,40)]
LABELS=['Green','Floor','Floor','Floor','Floor','Red']

class ColorScannerTests(unittest.TestCase):
 def replay(self,task,samples=SAMPLES,labels=LABELS):
  clock=SimpleNamespace(now=0)
  ns={'ast':ast,'re':re,'time':SimpleNamespace(time=lambda:clock.now)}
  exec(compile(ast.Module(body=FUNCTIONS,type_ignores=[]),str(SOURCE),'exec'),ns)
  code=(ROOT/f'solutions/module_4/{task}_reference.py').read_text()
  robot=SimpleNamespace(draw_info=lambda image:image,get_msg=lambda:None)
  verify=ns[task]
  with contextlib.redirect_stdout(io.StringIO()):
   _,state,_,_=verify(robot,None,None,code)
   for index,((r,g,b),label) in enumerate(zip(samples,labels)):
    clock.now=index+1
    message=f'Scan - R:{r} G:{g} B:{b}' if task=='color_sensor_basics' else f'Scan - {label} (Raw: R:{r} G:{g} B:{b})'
    robot.get_msg=lambda message=message:message
    _,state,_,_=verify(robot,None,state,code)
   robot.get_msg=lambda:None
   clock.now=20.1
   _,state,text,result=verify(robot,None,state,code)
   expected=result.copy()
   result['success']=not result['success']
   clock.now=100
   _,_,later_text,later=verify(robot,None,state,code)
   self.assertEqual(later,expected)
   self.assertEqual(later_text,text)
  return expected
 def test_measured_three_zones_pass(self):
  for task in ('color_sensor_basics','color_classification'):
   with self.subTest(task=task):self.assertTrue(self.replay(task)['success'])
 def test_all_floor_fails(self):
  for task in ('color_sensor_basics','color_classification'):
   with self.subTest(task=task):self.assertFalse(self.replay(task,[(107,85,60)]*6,['Floor']*6)['success'])
 def test_missing_red_fails(self):
  for task in ('color_sensor_basics','color_classification'):
   with self.subTest(task=task):self.assertFalse(self.replay(task,SAMPLES[:-1]+[(107,85,60)],LABELS[:-1]+['Floor'])['success'])
 def test_zero_is_not_a_valid_zone(self):
  self.assertFalse(self.replay('color_sensor_basics',[(0,0,0)]*6)['success'])
 def test_wrong_color_name_fails(self):
  self.assertFalse(self.replay('color_classification',SAMPLES,['Red','Floor','Floor','Floor','Green','Red'])['success'])
 def test_step_accepts_variable_names(self):
  ns={'ast':ast};exec(compile(ast.Module(body=FUNCTIONS,type_ignores=[]),str(SOURCE),'exec'),ns)
  self.assertTrue(ns['_has_scan_step']('gap=13\nrobot.move_forward_speed_distance(40,gap)'))
  self.assertTrue(ns['_has_scan_step']('gap=13\nrobot.move_forward_distance(gap)'))
  self.assertFalse(ns['_has_scan_step']('# robot.move_forward_distance(13)\npass'))
  self.assertFalse(ns['_has_scan_step']('robot.move_forward_speed_distance(40,10)'))

if __name__=='__main__':unittest.main()
