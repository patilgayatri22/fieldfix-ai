# Robotic Arm — Repair Guide

## Common Symptoms
- Arm drifts from commanded position over time
- Joints shudder or vibrate during slow movement
- Arm endpoint position inaccurate (off by fixed offset)
- One joint refuses to move
- Arm collapses or drops under gravity when powered off
- Excessive backlash (slop) in joint movement
- Arm overshoots target and oscillates
- Homing sequence fails or finds wrong position

## Likely Causes
- Position drift → servo/motor losing counts, PWM range not calibrated, mechanical slip
- Joint shudder → PID gain too high, signal noise, mechanical binding
- Fixed offset error → home position not set, kinematic parameters wrong in code
- Joint won't move → servo/motor fault (see servo_motor.md or dc_motor.md), broken wire at joint
- Drops under gravity → no holding torque (servo disabled), insufficient torque rated servo
- Backlash → worn gear train, loose coupler, play in joint bearing
- Overshoots → PID derivative gain too low, excessive speed, heavy payload
- Homing fails → limit switch fault, homing speed too high, switch wiring intermittent

## Safe First Checks
- Check each joint manually (powered off) — should move smoothly without hard spots
- Check all cable chains or drag chains for pinched or kinked wires at moving joints
- Verify limit switches trigger correctly by hand before powered homing
- Check mechanical fasteners at each joint — loose bolts cause positional error
- Check servo horns/couplers are tight — stripped horn screw causes slip

## Tools Needed
- Multimeter
- Set of hex/Allen keys
- Screwdrivers (Phillips and flat)
- Threadlocker (Loctite blue, for fasteners prone to vibration loosening)
- Servo tester

## Step-by-Step Guidance
1. Power off. Manually move each joint through full range. Note any stiff spots, grinding, or excessive play.
2. Tighten all joint fasteners. Check servo horn screw (center screw on servo output) — common point of slip.
3. Power on. Command each joint to home position. Check actual position matches expected.
4. If offset error is fixed (same amount every time) → adjust home offset value in firmware or re-run calibration routine.
5. If drift accumulates over time → check for gear slip or encoder miss-count (if using encoder feedback).
6. For joint shudder during slow movement → reduce PID proportional gain by 20%. Test again. Repeat until shudder stops.
7. For overshooting → increase PID derivative gain by 10% increments. If using velocity-based control, reduce max speed.
8. For joint that won't move → test that joint's servo/motor individually (see servo_motor.md). Check wiring continuity at cable chain bends — common break point.
9. For homing failure → manually trigger limit switch with finger. If controller doesn't detect it → check switch wiring. If switch OK → reduce homing speed.
10. For backlash → check gear mesh tightness. Many gearboxes have adjustment set screws. Apply minimal preload to take out play without adding friction.

## Stop Conditions
- **STOP** if arm moves unexpectedly at power-on without commanded movement — software/firmware fault, stand clear
- **STOP** if any joint makes cracking or loud grinding sounds — mechanical failure risk
- **STOP** if cable chain becomes tangled or pinched — stop and re-route before damage
- **STOP** if payload exceeds arm's rated capacity — joint damage and unpredictable movement
- Never put hands in arm workspace while powered unless emergency stop is confirmed active

## Prevention
- Run calibration routine before each use session
- Apply threadlocker to fasteners subject to vibration
- Inspect cable chains for wear every 50 operating hours
- Log joint position error after each run — growing error signals wear
- Store arm in home/neutral position to minimize spring load on joints

## Keywords
- robotic arm drift, arm calibration, joint position error, servo arm fault
- arm endpoint inaccuracy, joint backlash, arm overshoot, PID tuning robot arm
- homing failure, limit switch fault, arm collapses, robotic arm troubleshooting
- arm kinematic error, joint shudder, cable chain wiring fault
