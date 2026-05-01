# Stepper Motor — Repair Guide

## Common Symptoms
- Motor skips steps — position drifts over time
- Motor vibrates excessively without moving
- Motor stalls under light load
- Motor misses steps only at high speed
- Motor runs hot even at low duty cycle
- Motor moves in only one direction regardless of command
- Loud knocking or clunking during movement
- Motor holds position but won't rotate

## Likely Causes
- Step skipping → current too low, load too high, acceleration too aggressive
- Vibration without movement → coil wiring fault, driver malfunction
- Stalls under light load → coil current set too low, microstepping mismatch
- Misses steps at speed → acceleration ramp too steep, resonance zone
- Overheating → current set too high, idle current not reduced
- One-direction only → one coil pair wiring reversed or broken
- Knocking → driver pulse timing issue, missed steps accumulating
- Holds but won't rotate → enable pin not asserted, driver enable inverted

## Safe First Checks
- Check all 4 coil wires (or 6 for bipolar with center tap) for secure connection
- Measure coil resistance — both coil pairs should read equal resistance (typically 1–10Ω)
- Check driver current setting potentiometer or VREF voltage
- Check enable/disable signal from controller — stepper is disabled when enable pin is wrong state
- Manually rotate shaft while powered off — should have detents (small magnetic clicks)
- Check driver for overtemperature LED or thermal shutdown behavior

## Tools Needed
- Multimeter
- Small flathead screwdriver (for current trim pot)
- Stepper motor tester or microcontroller
- Oscilloscope (optional)

## Step-by-Step Guidance
1. Power off. Identify coil pairs using multimeter continuity. Coil A = two wires with resistance, Coil B = two other wires with resistance.
2. Confirm both coil pairs have matched resistance. Unequal → winding damage → replace motor.
3. Check driver VREF voltage. Set per formula: VREF = Motor_rated_current × 8 × Rsense (varies by driver — check datasheet).
4. Power on. Send slow step pulses. Motor should step cleanly at low speed.
5. If vibrates but doesn't rotate → swap one coil pair's wires. Coil polarity may be wrong.
6. If skips steps → lower acceleration in firmware. Increase current 10% at a time until steps are clean.
7. If overheating → enable driver's idle current reduction feature. Reduce to 50% hold current when stopped.
8. If stalls only at high speed → you're in resonance zone. Change microstepping setting (e.g., 1/8 to 1/16) or adjust speed to avoid resonance.
9. If motor won't rotate but holds → check enable pin. Many drivers require LOW to enable, HIGH to disable.
10. If all else fails → swap driver board. Stepper drivers are common failure points.

## Stop Conditions
- **STOP** if driver is too hot to touch — reduce current setting immediately before damage
- **STOP** if motor body temperature exceeds 80°C — thermal damage to windings
- **STOP** if any coil wire shows open circuit (infinite resistance) — winding broken, do not attempt repair, replace motor
- **STOP** if driver produces burning smell — disconnect power immediately

## Prevention
- Set driver current correctly before first use — never run at max current unnecessarily
- Enable idle current reduction for any application with long dwell times
- Use acceleration/deceleration ramps — never instant full-speed steps
- Keep stepper driver heatsink clear — never block airflow
- Match motor to load — stepper torque drops sharply at high speeds

## Keywords
- stepper motor skipping steps, stepper stalling, stepper vibration, stepper overheating
- NEMA 17 fault, NEMA 23 fault, A4988 driver, DRV8825 driver, TMC2208 stepper
- lost steps, position drift, coil resistance, VREF calibration, microstepping
- stepper motor troubleshooting, stepper not rotating, stepper resonance, enable pin
