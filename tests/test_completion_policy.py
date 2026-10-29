"""Moodle's selected activities keep matching lesson, simulator and tutor rules."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
EITHER={
    'welcome','test_drive','directional_movement','python_variables_commands',
    'maneuvering','sequential_navigation','defining_functions','for_loops',
    'conditional_logic','processing_sensor_data','arrays_and_elif','led_feedback',
    'simple_line_follower','art_of_debugging','hardware_safety_net','code_clinic','python_lists','concept_of_error',
    'upgraded_relay_controller','proportional_control',
}
HARDWARE={'license_to_drive','electric_motors','differential_drive','encoder_theory','intro_to_octoliner','telemetry','color_sensor_basics','color_classification','adaptive_speed'}

class CompletionPolicyTests(unittest.TestCase):
    def test_all_selected_activities_have_consistent_completion_rules(self):
        lessons={t['str_id']:t for m in json.loads((ROOT/'lessons-list.json').read_text()) for t in m['lessons']}
        sim=json.loads((ROOT/'simulation/manifest.json').read_text())['tasks']
        tutor=json.loads((ROOT/'tutor/generated/profiles.json').read_text())['tasks']
        self.assertEqual(len(EITHER|HARDWARE),29)
        for key in EITHER|HARDWARE:
            with self.subTest(task=key):
                mode='simulation-or-lab' if key in EITHER else 'simulation-and-lab'
                self.assertEqual(lessons[key]['executionMode'],mode)
                self.assertEqual(sim[key]['mode'],mode)
                self.assertEqual(tutor[key]['verification_rules']['execution_mode'],mode)
                text=(ROOT/lessons[key]['url'].split('/main/')[1]).read_text()
                self.assertTrue(text.startswith('---\n'))
                _, header, body = text.split('---', 2)
                self.assertNotIn('**Completion:**', header)
                self.assertIn('index:', header)
                self.assertIn('task:', header)
                self.assertIn('**Completion:**', body)
                rule=tutor[key]['verification_rules']['completion_requires']
                self.assertIn('simulator OR physical' if key in EITHER else 'successful physical verification',rule)
        self.assertEqual(lessons['sandbox']['executionMode'],'simulation-and-lab')
        self.assertEqual({key for key,t in lessons.items() if t['executionMode']=='simulation-or-lab'},EITHER)
