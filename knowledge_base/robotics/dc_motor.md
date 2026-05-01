# DC Motor — Repair Guide

## Common Symptoms
- Motor doesn't spin when powered
- Spins in wrong direction
- Motor runs but very slowly or weakly
- Excessive heat after short run time
- Sparking visible at brushes
- High-pitched whine or grinding noise
- Motor starts then stops repeatedly
- Shaft spins freely but no torque output

## Likely Causes
- No spin → broken wire, dead driver, no power
- Wrong direction → motor leads swapped, driver direction signal incorrect
- Weak torque → low supply voltage, high resistance connection, worn brushes
- Overheating → stall condition, undersized motor, driver current limit too high
- Sparking → worn carbon brushes, dirty commutator
- Whine → bearing failure or dry bearing
- Grinding → debris in motor, damaged bearing
- Spin but no torque → gearbox failure (if geared motor), not motor itself

## Safe First Checks
- Check power supply voltage at motor terminals under load — should be within spec
- Check all wiring connections for looseness, corrosion, or fraying
- Manually spin shaft by hand — should rotate smoothly with slight resistance
- Check motor driver for visible burn marks, swollen components, or smell
- Verify PWM duty cycle or analog voltage going to driver
- Feel motor body after 30 seconds — warm is OK, hot is a problem

## Tools Needed
- Multimeter
- Variable DC power supply (or PWM driver)
- Small flat-head screwdriver
- Wire brush or contact cleaner spray

## Step-by-Step Guidance
1. Power off. Disconnect motor from driver.
2. Apply rated voltage directly to motor terminals using bench supply. Motor should spin.
3. If motor spins correctly direct → problem is in driver or control signal, not motor.
4. If motor doesn't spin direct → check winding resistance with multimeter (typical 1–20Ω). Open circuit = dead winding = replace motor.
5. If weak torque → check supply voltage under load. Voltage should not drop more than 0.5V from no-load.
6. If voltage drop large → increase supply amperage capacity or shorten/thicken wiring.
7. For wrong direction → swap the two motor wires at the driver output terminals (or reverse direction signal in software).
8. For sparking → inspect brush condition. If brushes worn below 3mm, replace brushes or motor.
9. For grinding/whine → apply one drop of light machine oil to shaft bearing. Retest. If noise persists → replace motor.
10. For overheating → verify load is within motor's rated torque. Reduce load or add cooling.

## Stop Conditions
- **STOP** if motor casing is too hot to touch (>60°C) — thermal failure risk
- **STOP** if you see sparks outside the motor body (not just at brushes) — fire risk
- **STOP** if motor smells like burning varnish — winding insulation failing
- **STOP** if winding resistance reads 0Ω (short circuit) — do not power, replace motor
- Do not operate stalled motor under power for more than 5 seconds

## Prevention
- Run motor within rated voltage and current at all times
- Add a fuse or current-limiting circuit to protect driver and motor
- Keep motor vents clear — never cover or obstruct airflow
- Inspect brush condition every 50 hours of use on brushed motors
- Consider brushless motors for high-cycle applications

## Keywords
- DC motor not spinning, motor wrong direction, motor weak torque, motor overheating
- brushed motor repair, motor driver fault, PWM motor control, motor winding resistance
- motor sparking, commutator wear, brush replacement, DC motor troubleshooting
- geared motor no torque, motor stall, motor wiring fault
