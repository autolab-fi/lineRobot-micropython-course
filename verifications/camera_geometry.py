"""Convert physical route lengths into the existing camera coordinate system.

HAMK's black AprilTag square is 75.9079 mm in the original print PDF.
Keep reset/dock/map coordinates untouched: only relative route displacements
use this metric, frozen from the starting tag observation. This assumes the
printed tag retains the PDF scale; it is not a floor-plane homography.
"""
import math

TAG_SIDE_CM = 7.590785625555558


def route_targets(info, route):
    """Return reverse-ordered camera waypoints, or None for an invalid tag."""
    names = ('bottom_right', 'bottom_left', 'top_left', 'top_right')
    try:
        corners = [tuple(float(v) for v in info[name]) for name in names]
        position = tuple(float(v) for v in info['position'])
        if any(len(p) != 2 or not all(math.isfinite(v) for v in p)
               for p in [*corners, position]):
            return None
    except (KeyError, TypeError, ValueError):
        return None
    br, bl, tl, tr = corners
    sides = [math.dist(corners[i], corners[(i + 1) % 4]) for i in range(4)]
    if min(sides) <= 0 or max(sides) / min(sides) > 1.3:
        return None
    forward = tuple((tl[i] + tr[i] - bl[i] - br[i]) / (2 * TAG_SIDE_CM) for i in range(2))
    right = tuple((tr[i] + br[i] - tl[i] - bl[i]) / (2 * TAG_SIDE_CM) for i in range(2))
    nf, nr = math.hypot(*forward), math.hypot(*right)
    if min(nf, nr) <= 0 or max(nf, nr) / min(nf, nr) > 1.3:
        return None
    if abs(sum(a*b for a, b in zip(forward, right))) / (nf*nr) > .25:
        return None
    if forward[0]*right[1] - forward[1]*right[0] <= 0:
        return None
    point = list(position)
    heading = 0.0
    targets = []
    for step in route:
        if isinstance(step, dict):
            distance = step['forward'] - step['backward']
            for i in range(2):
                point[i] += distance * (math.cos(heading)*forward[i] + math.sin(heading)*right[i])
            targets.append(tuple(point))
        else:
            heading += math.radians(step[0]['right'] - step[0]['left'])
    return targets[::-1]
