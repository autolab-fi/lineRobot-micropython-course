# Lesson 1: Fog of War Survey

## Lesson objective
Guide the robot through a repeatable snake pattern that uncovers at least 90% of a hidden map image.

## Introduction
Mission Control shares a map image of a cloudy landing zone. Your robot has to sweep the area without manual steering, revealing almost the entire map through a predictable path. Instead of micromanaging every turn, you will rely on a simple boustrophedon (snake) pattern that alternates direction each row so you waste no time repositioning.

## Theory

### Why a snake pattern works
A snake sweep reduces dead time because the robot reaches the end of one row and immediately starts the next in the opposite direction. This keeps motion continuous and avoids long reposition arcs.

### Breaking the field into passes
Decide how many straight passes you need based on the map image dimensions. Each pass should span the usable width of the map so neighbouring lines slightly overlap. Store the pass length and the small step that moves you down to the next row so you can reuse them in a loop.

### Tracking revealed area
Keep a running counter of how many passes are complete versus the total planned. The simplest completion check is `coverage = (completed_passes / total_passes) * 100`. Stop once coverage reaches or exceeds 90% so the rover does not overrun its mission boundary.

### Loading the map asset
You can visualise progress against the provided map image:

```python
MAP_PATH = "images/module_9/fog_map.png"

# Load or display this image however your environment prefers.
# For example, you might show it on a dashboard while the robot sweeps.
```

## Assignment
Write a program that:

- Loads the provided map image from `images/module_9/fog_map.png` so you can refer to the mission area while debugging.
- Defines two helpers: one to drive a full horizontal pass and one to step down to the next row.
- Uses a loop to alternate direction each pass, creating a continuous snake pattern until at least **90%** of the planned passes are finished.
- Logs the coverage percentage after each pass and reports the final percentage when the loop ends.

## Conclusion
You used a simple, repeatable movement plan to uncover nearly the entire map with minimal wasted turns. This pattern is reliable whenever you need broad coverage without complex path planning.
