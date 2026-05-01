# Servo Motor — Repair Guide

## Common Symptoms
- Continuous buzzing or humming at rest or under load
- Jittery, twitchy movement that won't settle
- Servo doesn't move when commanded
- Moves to wrong position or overshoots
- Overheating casing after short use
- Grinding or clicking noise during rotation
- Partial range of motion only
- Servo moves on its own without command signal

## Likely Causes
- Buzzing at rest → PWM signal out of range or incorrect pulse width
- Jitter → electrical noise on signal wire, loose connector, underpowered supply
- No movement → no signal, disconnected wire, dead motor winding
- Wrong position → PWM library misconfigured, incorrect min/max pulse values
- Overheating → mechanical binding, stall condition, undersized servo for load
- Grinding noise → stripped or cracked plastic gear
- Partial range → physical obstruction, PWM range not calibrated
- Moving without command → floating signal line (no pull-down resistor)

## Safe First Checks
- Check all three wires: power (red), ground (black/brown), signal (orange/yellow/white)
- Confirm supply voltage matches servo spec (typically 4.8V–6V for hobby, up to 7.4V for high-torque)
- Wiggle connector at both ends — check for intermittent contact
- Remove mechanical load (disconnect linkage/arm) and test servo bare
- Feel casing after 30 seconds of operation — should not be hot to touch
- Listen for gear grinding before visual inspection

## Tools Needed
- Multimeter (voltage measurement)
- Servo tester or microcontroller with PWM output
- Oscilloscope (optional, for signal verification)
- Small Phillips/JIS screwdriver
- Calipers (optional, for gear wear measurement)

## Step-by-Step Guidance
1. Power off robot. Disconnect servo signal wire from controller.
2. Measure supply voltage at servo connector. Should match servo spec ±0.2V.
3. Reconnect signal wire. Use a servo tester to send a known-good PWM signal (1500µs center).
4. If servo responds correctly to tester → problem is in controller/code PWM values. Recalibrate min/max pulse width.
5. If still buzzing with tester → check mechanical load. Remove arm and retest.
6. If buzzing stops without load → servo is stalling. Reduce load or upgrade servo torque rating.
7. If no movement at all → test continuity on all three wires from controller to servo.
8. If wires OK but no movement → servo motor winding or driver IC is dead. Replace servo.
9. If grinding noise → open servo case (4 screws on bottom). Inspect gear train for cracked/stripped teeth. Replace gear set if available, otherwise replace servo.
10. For jitter → add 100µF capacitor across power/ground near servo. Ensure signal wire is away from motor wires. Use shielded cable if possible.

## Stop Conditions
- **STOP** if servo casing is too hot to hold for 3 seconds — thermal damage risk, power off immediately
- **STOP** if you smell burning plastic or see smoke — disconnect power
- **STOP** if supply voltage is above servo maximum rating — overvoltage destroys servo electronics
- **STOP** if gear grinding worsens — continuing causes full gear failure
- Do not force servo past mechanical end-stops — permanent damage to gears

## Prevention
- Always calibrate PWM min/max values before first use
- Match servo torque rating to actual load — add 30% safety margin
- Use capacitors on servo power lines to suppress noise
- Secure all connectors with strain relief or cable tie
- Do not stall servo against hard stops for more than 1 second
- Lubricate metal gear servos annually with light grease

## Keywords
- servo buzzing, servo jitter, servo not moving, servo overheating, servo grinding
- PWM out of range, pulse width calibration, servo tester, servo stall
- hobby servo repair, RC servo fault, servo gear stripped, servo signal noise
- servo motor troubleshooting, servo arm drift, servo clicking
