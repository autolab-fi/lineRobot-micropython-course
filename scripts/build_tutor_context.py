#!/usr/bin/env python3
"""Build the opt-in AI profile manifest; lesson prose is maintained separately."""
import argparse
import ast
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = 'https://github.com/autolab-fi/lineRobot-micropython-course'
RAW = 'https://raw.githubusercontent.com/autolab-fi/lineRobot-micropython-course/main/'


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def checker_details(source, task_id):
    tree = ast.parse(source)
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == task_id)
    constants = {}
    for node in ast.walk(function):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    try:
                        value = ast.literal_eval(node.value)
                        constants[target.id] = sorted(value) if isinstance(value, set) else value
                    except (ValueError, TypeError):
                        pass
    return ast.get_docstring(function) or '', constants


def build(check=False):
    lessons = [t for m in json.loads((ROOT/'lessons-list.json').read_text()) for t in m['lessons']]
    notes = json.loads((ROOT/'tutor/task-notes.json').read_text())['tasks']
    sim = json.loads((ROOT/'simulation/manifest.json').read_text())['tasks']
    metadata = json.loads((ROOT/'simulation/generated/task-metadata.json').read_text())['tasks']
    active = {t['str_id'] for t in lessons}
    assert active <= set(notes) and active <= set(sim), 'Active task coverage differs'
    profiles = {}
    changed = []
    for lesson in lessons:
        key = lesson['str_id']; note = notes[key]
        path = ROOT / lesson['url'].split('/main/', 1)[1]
        text = path.read_text()
        reference = (ROOT/note['reference']).read_text()
        ast.parse(reference)
        meta = metadata[key]
        checker_path = meta['verificationFile']
        checker = (ROOT/checker_path).read_text()
        description, constants = checker_details(checker, key)
        summary = re.sub(r'\s+', ' ', re.sub(r'```.*?```', '', text, flags=re.S))[:2000]
        validation = note['physicalValidation']
        rules = {
            'physical_start': meta.get('physicalStart'),
            'physical_checker_constants': constants,
            'simulator_checks': sim[key].get('checks', []),
            'physical_validation': validation,
            'starting_parameters': note['parameters'],
            'execution_mode': lesson['executionMode'],
            'completion_requires': 'successful physical verification; simulation is practice',
            'simulator_limitations': 'Simulated RGB samples do not reproduce all HAMK illumination/tape overlap. Timed motor motion and reset behavior need physical validation.',
            'do_not_reveal': ['full reference solution', 'raw checker implementation', 'hidden test thresholds'],
        }
        if note.get('colorGuidance'):
            rules['published_color_guidance'] = note['colorGuidance']
        refs = {'context_manifest_schema': 1, 'course_repo_url': REPO, 'task_url': lesson['url'],
                'reference_url': RAW + note['reference'], 'guidance_updated': note['guidanceUpdated'],
                'source_sha256': {'lesson': digest(text), 'template': digest(lesson['template']),
                                  'reference': digest(reference), 'checker': digest(checker),
                                  'simulation': digest(json.dumps(sim[key], sort_keys=True))}}
        if note.get('calibrationPolicy'):
            rules['calibration_policy'] = note['calibrationPolicy']
        if note.get('simulationReference'):
            simulation_reference = (ROOT/note['simulationReference']).read_text()
            ast.parse(simulation_reference)
            refs['simulation_reference_url'] = RAW + note['simulationReference']
            refs['source_sha256']['simulation_reference'] = digest(simulation_reference)
        profiles[key] = {
            'assignment_full_text': text, 'assignment_summary': summary,
            'reference_solution_text': reference,
            'verification_summary': '\n'.join(filter(None, [description, 'Hardware evidence: ' + json.dumps(validation),
                'The physical and simulator checks are distinct; consult their labeled rules. Reset failures before student execution are infrastructure failures. Do not infer a student-code failure from reset or video delivery alone. Provide hints rather than a complete solution.'])),
            'verification_rules': rules, 'common_mistakes': note['commonMistakes'],
            'repo_refs': refs, 'checker_source_ref': RAW + checker_path,
        }
    output = ROOT/'tutor/generated/profiles.json'
    encoded = json.dumps({'schemaVersion': 1, 'courseRepoUrl': REPO, 'tasks': profiles}, indent=2, ensure_ascii=False) + '\n'
    if not output.exists() or output.read_text() != encoded:
        changed.append(str(output.relative_to(ROOT)))
        if not check:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(encoded)
    if check and changed:
        raise SystemExit('Stale generated content: ' + ', '.join(changed))
    print(f'{len(profiles)} profiles; {len(changed)} files ' + ('need updates' if check else 'updated'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
