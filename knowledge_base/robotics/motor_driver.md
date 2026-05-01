# Motor Driver — Repair Guide (L298N / L293D / BTS7960 / DRV8833)

## Common Symptoms
- Motor doesn't respond despite correct command signals
- Driver board gets very hot quickly
- One motor channel works, other doesn't
- Motor only runs at full speed (no PWM speed control)
- Direction commands ignored — motor spins one way only
- Driver shuts down after a few seconds (thermal protection)
- Motor runs but twitches or stutters at low speed
- Burning smell from driver board

## Likely Causes
- No response → enable pin not active, logic supply missing, blown driver IC
- Overheating → motor stall, current too high, no heatsink, undersized driver
- One channel dead → blown half-bridge on that channel, internal short
- No speed control → PWM signal not reaching driver's ENA/ENB pin
- Direction stuck → IN1/IN2 pins not toggling, software logic error
- Thermal shutdown → load current exceeds driver rating (L298N: 2A per channel max)
- Stuttering at low speed → PWM frequency too low (below 1kHz causes audible stutter)
- Burning smell → driver IC is dead — stop immediately

## Safe First Checks
- Check 5V logic supply voltage at driver's Vss/logic-in pin
- Check motor supply voltage at Vs/Vmot pin — should match motor rating
- Verify ENA and ENB pins are HIGH (or PWM signal present) for enabled channels
- Check IN1, IN2, IN3, IN4 signal levels with multimeter or LED test
- Touch driver IC carefully after 10 seconds — should be warm, not burning hot
- Check for visible burn marks, darkened areas, or cracked IC package

## Tools Needed
- Multimeter
- LED + resistor (signal level tester)
- Small screwdriver
- Heatsink compound (thermal paste) if reseating heatsink

## Step-by-Step Guidance
1. Power off. Verify all wiring per driver datasheet pinout.
2. Power on (no motor connected). Measure logic supply (5V pin) and motor supply (Vmot pin). Both must be present.
3. Set IN1=HIGH, IN2=LOW, ENA=HIGH. Measure OUT1 and OUT2 with multimeter. Should show motor supply voltage differential.
4. If OUT voltage correct → reconnect motor. If motor still doesn't run → motor fault (see dc_motor.md).
5. If OUT voltage zero on both channels → driver IC blown. Replace board.
6. If only one channel dead → use remaining channel if available, or replace board.
7. For overheating → attach heatsink to driver IC if not already present. Reduce motor current load. Upgrade to higher-rated driver.
8. For no speed control → confirm ENA pin is connected to PWM output, not tied to 5V. Set PWM frequency to 5–20kHz.
9. For stuttering at low speed → increase PWM frequency in code. Most drivers work best at 10–20kHz.
10. For direction stuck → test IN1/IN2 pins directly with 5V wire. If motor direction then works → software/control signal fault, not driver.

## Stop Conditions
- **STOP** if driver smells like burning — disconnect power immediately, IC is dead
- **STOP** if driver IC is too hot to touch after 10 seconds — thermal shutdown imminent, check load
- **STOP** if motor supply voltage is reversed — many drivers are not reverse-polarity protected
- **STOP** if Vmot exceeds driver maximum (L298N: 46V, L293D: 36V, DRV8833: 11V) — overvoltage destroys IC instantly
- Do not exceed driver's rated current — L298N max 2A per channel, L293D max 600mA per channel

## Prevention
- Always attach heatsink to L298N — it runs hot by design (voltage drop method)
- Use flyback diodes on motor terminals if not built into driver
- Add motor supply capacitor (100µF–1000µF) near driver Vmot pin
- Choose driver with current rating 2× your motor's stall current
- Separate motor supply and logic supply — shared supply causes noise and resets

## Keywords
- motor driver not working, L298N fault, L293D fault, DRV8833, BTS7960
- motor driver overheating, H-bridge failure, enable pin, IN1 IN2 direction
- PWM speed control not working, motor driver burned, motor channel dead
- motor driver troubleshooting, H-bridge driver, motor controller fault
