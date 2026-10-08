import ast
import contextlib
import io
import math
import os
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'verifications/module_2.py'
FUNCTION=next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='electric_motors')
CODE='robot.run_motors_speed(30, 30)\nrobot.stop()'

class ElectricMotorsTests(unittest.TestCase):
    def run_positions(self,positions,code=CODE,scale=22/2.54):
        clock=SimpleNamespace(now=0)
        def no_image(path):raise OSError('No image in unit test')
        ns={'ast':ast,'os':os,'__file__':str(SOURCE),'time':SimpleNamespace(time=lambda:clock.now),'cv2':SimpleNamespace(imread=no_image)}
        exec(compile(ast.Module(body=[FUNCTION],type_ignores=[]),str(SOURCE),'exec'),ns)
        robot=SimpleNamespace(position=(30,50),draw_info=lambda x:x,pixels_to_cm=lambda x:x/scale,delta_points=lambda a,b:math.dist(a,b))
        robot.get_info=lambda:{'position':robot.position}
        with contextlib.redirect_stdout(io.StringIO()):
            _,td,_,_=ns['electric_motors'](robot,None,None,code)
        self.assertEqual(td['data']['flag-coords'],(int(46*scale),int(115*scale)))
        for t,position in positions:
            clock.now=t;robot.position=position
            _,td,_,result=ns['electric_motors'](robot,None,td,code)
        clock.now=12
        _,_,_,later=ns['electric_motors'](robot,None,td,code)
        self.assertEqual(result,later)
        return result

    def test_target_is_in_centimeters_at_different_camera_scales(self):
        for scale in (22/2.54,44/2.54):
            self.assertTrue(self.run_positions([(5,(115,46)),(8,(115,46)),(9.5,(115,46))],scale=scale)['success'])

    def test_old_simulator_goal_does_not_pass(self):
        self.assertFalse(self.run_positions([(5,(50,20)),(9.5,(50,20))])['success'])

    def test_passing_through_target_without_stopping_fails(self):
        self.assertFalse(self.run_positions([(5,(115,46)),(8,(130,46)),(9.5,(130,46))])['success'])
        self.assertFalse(self.run_positions([(8,(106,46)),(9.5,(115,46))])['success'])

    def test_missing_calls_and_fake_output_fail(self):
        for code in ['pass','print("run_motors_speed stop")','robot.move_forward_distance(85)\nrobot.stop()']:
            self.assertFalse(self.run_positions([(5,(115,46)),(9.5,(115,46))],code=code)['success'])

    def test_lost_camera_cannot_pass_with_stale_target(self):
        self.assertFalse(self.run_positions([(5,(115,46)),(6,(115,46)),(9.5,None)])['success'])
