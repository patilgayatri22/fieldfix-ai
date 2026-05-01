# Proximity & Line Sensors — Repair Guide (Ultrasonic / IR / Line Following)

## Common Symptoms
- Ultrasonic sensor always reads max distance (no detection)
- Ultrasonic reads 0 or very small values constantly
- IR sensor doesn't trigger near objects
- IR sensor triggers constantly even with no obstacle
- Line following robot veers off track
- Line sensor reads same value on all surfaces
- Sensor output fluctuates wildly
- Sensor works indoors but fails in sunlight

## Likely Causes
- Max distance reading → trigger pulse not sent, target surface absorbs ultrasound (soft/angled)
- Always 0 → echo pin flooded, sensor too close, wiring fault
- IR no trigger → LED burned out, sensitivity pot misadjusted, object out of range
- IR always triggered → ambient IR interference, sensitivity too high, direct light hitting receiver
- Line sensor veers → uneven sensor height, one sensor failed, threshold not calibrated
- Same value all surfaces → sensor not powered, output wire broken
- Wild fluctuation → electrical noise, supply voltage unstable
- Fails in sunlight → IR ambient light saturation (common for analog IR sensors)

## Safe First Checks
- Measure supply voltage at sensor (usually 3.3V or 5V)
- For ultrasonic (HC-SR04): confirm TRIG and ECHO pins are not swapped
- For IR: check sensitivity potentiometer (small blue trim pot on module) — turn slowly each direction
- For line sensor: hold sensor 1–2cm above a white surface, then a black surface — output should differ
- Check for physical damage to sensor face (cracks, dirt, condensation)
- Verify sensor output is connected to correct GPIO input type (digital vs. analog)

## Tools Needed
- Multimeter
- Small flat-head screwdriver (for trim pot)
- Serial monitor or oscilloscope for output testing

## Step-by-Step Guidance
1. Power sensor module. Measure VCC pin — must match spec (3.3V or 5V).
2. For ultrasonic HC-SR04: send 10µs pulse on TRIG. Measure ECHO pin — should go HIGH for duration proportional to distance (58µs per cm).
3. If ECHO never goes HIGH → check TRIG pulse is reaching sensor. If TRIG OK but ECHO silent → sensor dead, replace.
4. If reading 0 always → target is too close (HC-SR04 minimum range ~2cm). Move target farther.
5. For IR obstacle sensor: power on, hold white paper at 10cm. LED on module should light. Adjust trim pot until LED triggers reliably.
6. If IR sensor triggers in open air → sensitivity set too high. Turn trim pot to reduce sensitivity until no false trigger.
7. For IR failure in sunlight → shield sensor from direct light. Use digital IR sensors with modulation (38kHz) for sunlight immunity.
8. For line sensors: place sensor array over line. Calibrate in code by reading min/max values on white and black surface. Set threshold at midpoint.
9. If one sensor in array always reads same value → that sensor is dead. Swap position to verify, then replace module.
10. For noisy readings → add 100nF decoupling capacitor on sensor VCC pin. Check for nearby motor interference.

## Stop Conditions
- **STOP** if sensor supply voltage is reversed — most ICs not reverse-polarity protected
- **STOP** if sensor output wire is shorted to motor power line — damages microcontroller GPIO
- Do not stare directly into IR emitter LED for extended periods

## Prevention
- Mount ultrasonic sensors away from vibrating motors — vibration causes false echoes
- Shield IR line sensors with opaque side walls to reduce ambient light interference
- Calibrate line sensors at start of each run in actual lighting conditions
- Secure all sensor mounting so height above surface remains consistent
- Use I2C distance sensors (VL53L0X, etc.) for applications needing sunlight immunity

## Keywords
- ultrasonic sensor not working, HC-SR04 fault, IR sensor always on, IR sensor not detecting
- line sensor not working, line following robot fault, proximity sensor calibration
- sensor noise, sensor false trigger, ambient light interference, trim pot adjustment
- sensor troubleshooting, ultrasonic always max, IR module repair
