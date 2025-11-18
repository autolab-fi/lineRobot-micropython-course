# Lesson 2.7: Multi-Point Mineral Survey

## Lesson Objective
Navigate to 5 different scanning zones, activate the detection system at each location for 2 seconds to reveal minerals, wait 3 seconds for collection, then proceed to the next zone.

## Introduction
Mission Control has identified 5 mineral-rich zones in your survey area. Your robot must systematically visit each zone, activate its scanner LEDs to reveal what minerals are present, wait for the collection system to gather samples, then move to the next location. This multi-waypoint survey mission requires precise timing and navigation.

## Theory

### Survey Zone Map
The exploration area is divided into 5 distinct scanning zones. Each zone may contain different mineral deposits that will only be revealed when your scanner is active.

![Survey Zones](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_9/survey_zones.png?raw=true)

Study the zone layout carefully. Your robot must visit each numbered zone in sequence, performing a complete scan and collection cycle at each stop.

### Multi-Waypoint Navigation
Instead of scanning from one position, you'll move between 5 different zones. Each zone requires the same scanning procedure:
1. Navigate to the zone center
2. Activate scanner (turn LEDs ON)
3. Hold for 2 seconds (mineral detection phase)
4. Turn LEDs OFF
5. Wait 3 seconds (mineral collection phase)
6. Move to next zone

### Timing Requirements
The scanner requires exactly **2 seconds of LED activation** to properly analyze the mineral composition at each zone. After detection, the collection mechanism needs **3 seconds** to extract the sample. These timing windows are critical for accurate data collection.

**Per-zone timing:**
- LEDs ON: 2.0 seconds (±0.2 seconds)
- LEDs OFF: 3.0 seconds (±0.3 seconds)
- Total per zone: ~5 seconds
- Total mission: ~25 seconds for all 5 zones

## Assignment
Write a program that:

1. Visits all **5 scanning zones** shown in the zone map using movement functions
2. At each zone:
   - **Stop at the zone center** (robot must be stationary during scanning)
   - **Turn LEDs ON** to activate the mineral scanner
   - **Keep LEDs ON for exactly 2 seconds** (mineral detection phase)
   - **Turn LEDs OFF** after scanning completes
   - **Wait 3 seconds** with LEDs off (mineral collection phase)
3. Moves to the next zone after collection completes
4. Repeats until all 5 zones are surveyed

**Requirements:**
- Must visit all 5 zones in sequence
- LEDs must be ON for 2 seconds at each zone
- LEDs must be OFF for 3 seconds at each zone (collection time)
- Scanner must be active (LEDs ON) for at least 40% of total mission time
- Complete the mission within the time limit
- Use `time.sleep()` for precise timing control

## Conclusion
You've programmed a systematic multi-zone survey mission that combines navigation, precise timing control, and repeated procedures. This type of mission is essential in planetary exploration where rovers must survey multiple sites efficiently while managing power and time constraints.
