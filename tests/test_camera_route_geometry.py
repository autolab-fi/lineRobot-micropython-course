import importlib.util
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('camera_geometry', ROOT/'verifications/camera_geometry.py')
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)
ROUTE = [{'forward':35,'backward':0}, [{'left':90,'right':0}],
         {'forward':25,'backward':0}, [{'left':0,'right':90}],
         {'forward':35,'backward':0}, [{'left':0,'right':90}],
         {'forward':25,'backward':0}]


def info(scale=.9, heading=0):
    c,s=math.cos(heading),math.sin(heading)
    def point(x,y):return (37+scale*(c*x-s*y),60+scale*(s*x+c*y))
    half=geometry.TAG_SIDE_CM/2
    return {'position':(37,60),'bottom_right':point(-half,half),
            'bottom_left':point(-half,-half),'top_left':point(half,-half),
            'top_right':point(half,half)}


class CameraRouteGeometryTests(unittest.TestCase):
    def test_physical_lengths_keep_camera_origin_unchanged(self):
        targets=geometry.route_targets(info(),ROUTE)[::-1]
        expected=[(68.5,60),(68.5,37.5),(100,37.5),(100,60)]
        for actual,target in zip(targets,expected):
            self.assertAlmostEqual(actual[0],target[0]);self.assertAlmostEqual(actual[1],target[1])

    def test_rotated_camera_basis_and_reverse(self):
        p=geometry.route_targets(info(.8,math.pi/2),[{'forward':0,'backward':20}])
        self.assertAlmostEqual(p[0][0],37);self.assertAlmostEqual(p[0][1],44)

    def test_original_pixel_observation_does_not_use_encoder_or_nominal_dpi(self):
        corners=[[292,545],[290,486],[350,485],[351,545]]
        keys=('bottom_right','bottom_left','top_left','top_right')
        d={k:tuple(v*2.54/22 for v in p) for k,p in zip(keys,corners)}
        d['position']=(37.00318,59.51682)
        endpoint=geometry.route_targets(d,ROUTE)[0]
        self.assertLess(math.dist(endpoint,(100.4,59.0)),1)
        self.assertGreater(math.dist(endpoint,(107,59)),6)

    def test_missing_nonfinite_degenerate_or_mirrored_tag_rejected(self):
        variants=[{},info(),info(),info(),info()]
        variants[1]['top_left']=None
        variants[2]['position']=(float('nan'),0)
        variants[3].update({k:(0,0) for k in ('top_left','top_right','bottom_left','bottom_right')})
        variants[4]['top_left'],variants[4]['bottom_right']=variants[4]['bottom_right'],variants[4]['top_left']
        for value in variants:
            with self.subTest(value=value):self.assertIsNone(geometry.route_targets(value,ROUTE))



class RouteCheckerTests(unittest.TestCase):
    def replay(self, task, variant):
        import sys
        from types import SimpleNamespace
        from unittest.mock import patch
        import contextlib,io
        sys.path.insert(0,str(ROOT/'verifications'))
        try:
            module=__import__('module_1' if task=='sequential_navigation' else 'module_11')
            clock=SimpleNamespace(now=0)
            details=info()
            robot=SimpleNamespace(get_info=lambda:details,draw_info=lambda image:image,
                                  cm_to_pixel=lambda x:round(x*22/2.54))
            reference='solutions/module_1/sequential_navigation_reference.py' if task=='sequential_navigation' else 'solutions/module_11/navigation_reference.py'
            code=(ROOT/reference).read_text() if variant!='empty' else 'pass'
            checker=getattr(module,task)
            with patch.object(module,'time',SimpleNamespace(time=lambda:clock.now)),patch.object(module.cv2,'imread',return_value=None),contextlib.redirect_stdout(io.StringIO()):
                _,td,_,_=checker(robot,None,None,code)
                targets=list(reversed(td['data']['targets']))
                if variant=='skip':targets=targets[-1:]
                if variant=='reverse':targets=targets[::-1]
                if variant=='too_long':targets=[(37+1.5*(x-37),60+1.5*(y-60)) for x,y in targets]
                for p in targets:
                    clock.now+=2;details['position']=p
                    _,td,_,_=checker(robot,None,td,code)
                clock.now=td['end_time']+1
                _,td,_,result=checker(robot,None,td,code)
                return result
        finally:sys.path.pop(0)

    def test_reference_route_and_negative_routes(self):
        for task in ('sequential_navigation','navigation'):
            for variant in ('correct','skip','reverse','too_long','empty'):
                with self.subTest(task=task,variant=variant):
                    self.assertEqual(self.replay(task,variant)['success'],variant=='correct')

if __name__=='__main__':unittest.main()
