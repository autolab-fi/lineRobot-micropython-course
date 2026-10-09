"""Full module 6 requirements, combined MQTT deliveries and recorded HAMK runs."""
import ast,contextlib,io,json,math,os,re
from pathlib import Path
from types import SimpleNamespace
import unittest
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'verifications/module_6.py'
FUNCTIONS=[n for n in ast.parse(SOURCE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ('art_of_debugging','hardware_safety_net','code_clinic')]
class Module6Requirements(unittest.TestCase):
 def replay(self,task,events,valid=True):
  clock=SimpleNamespace(now=0);messages=[]
  ns={'ast':ast,'math':math,'os':os,'re':re,'__file__':str(SOURCE),'time':SimpleNamespace(time=lambda:clock.now),'cv2':SimpleNamespace(imread=lambda *a:None,IMREAD_UNCHANGED=-1)}
  exec(compile(ast.Module(body=FUNCTIONS,type_ignores=[]),str(SOURCE),'exec'),ns)
  robot=SimpleNamespace(position=(50,30),position_px=None,draw_info=lambda f:f,get_msg=lambda:messages.pop(0) if messages else None)
  code=(ROOT/f'solutions/module_6/{task}_reference.py').read_text() if valid else 'pass';verify=ns[task]
  with contextlib.redirect_stdout(io.StringIO()):_,state,_,_=verify(robot,None,None,code)
  for event in events:
   if 'pose' in event:robot.position=event['pose']
   if 'message' in event:messages.append(event['message'])
   clock.now+=.01;_,state,_,_=verify(robot,None,state,code)
  clock.now=state['end_time']+.1;_,state,text,result=verify(robot,None,state,code)
  expected=result.copy();result['success']=not result['success'];clock.now+=10
  robot.position=(80,30);_,state,later_text,later=verify(robot,None,state,code)
  self.assertEqual(expected,later);self.assertEqual(text,later_text)
  return expected
 def safety(self,count=10,unknowns=4,complete=True,duplicate=False,valid=True):
  lines=[]
  for i in range(1,count+1):lines.append(f"Sector #{1 if duplicate else i} | RGB: (0,0,0)\nANALYSIS: {'Unknown' if i<=unknowns else 'Floor'}")
  if complete:lines.append('Survey Complete')
  return self.replay('hardware_safety_net',[{'message':'\n'.join(lines)}],valid)
 def clinic(self,points,message='Mineral Detected: Green',valid=True):return self.replay('code_clinic',[*[{'pose':p} for p in points],{'message':message}],valid)
 def test_all_safety_events_in_one_delivery_pass(self):self.assertTrue(self.safety()['success'])
 def test_incomplete_scans_fail(self):self.assertFalse(self.safety(count=8)['success'])
 def test_missing_shadow_zone_fails(self):self.assertFalse(self.safety(unknowns=3)['success'])
 def test_duplicate_sector_does_not_inflate_scan_count(self):self.assertFalse(self.safety(duplicate=True)['success'])
 def test_missing_completion_fails(self):self.assertFalse(self.safety(complete=False)['success'])
 def test_prints_without_required_code_fail(self):self.assertFalse(self.safety(valid=False)['success'])
 def test_clinic_full_route_and_color_pass(self):self.assertTrue(self.clinic([(80,30),(105,60),(60,90)])['success'])
 def test_clinic_partial_route_fails(self):self.assertFalse(self.clinic([(80,30),(105,60)])['success'])
 def test_clinic_no_color_fails(self):self.assertFalse(self.clinic([(80,30),(105,60),(60,90)],'')['success'])
 def test_no_minerals_message_is_not_a_detection(self):self.assertFalse(self.clinic([(80,30),(105,60),(60,90)],'No minerals found')['success'])
 def test_clinic_invalid_code_cannot_pass_with_motion(self):self.assertFalse(self.clinic([(80,30),(105,60),(60,90)],valid=False)['success'])
 def test_debugging_full_route_passes(self):self.assertTrue(self.replay('art_of_debugging',[{'pose':(80,30)},{'pose':(105,60)}])['success'])
 def test_debugging_partial_route_fails(self):self.assertFalse(self.replay('art_of_debugging',[{'pose':(80,30)}])['success'])
 def test_debugging_invalid_code_cannot_pass_with_motion(self):self.assertFalse(self.replay('art_of_debugging',[{'pose':(80,30)},{'pose':(105,60)}],False)['success'])
 def test_recorded_hamk_runs_pass_stricter_requirements(self):
  for sid in (22072,22073,22084,22085):
   with self.subTest(submission=sid):
    fixture=json.loads((ROOT/f'tests/fixtures/hamk-{sid}.json').read_text())
    result=self.replay(fixture['task'],fixture['events']);self.assertTrue(result['success']);self.assertEqual(result['score'],100)
 def test_previous_lower_straight_route_does_not_skip_new_checkpoint_order(self):
  fixture=json.loads((ROOT/'tests/fixtures/hamk-22071.json').read_text())
  self.assertFalse(self.replay(fixture['task'],fixture['events'])['success'])
if __name__=='__main__':unittest.main()
