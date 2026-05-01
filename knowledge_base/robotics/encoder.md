# Encoder — Repair Guide (Quadrature / Hall Effect / Optical)

## Common Symptoms
- Encoder reads zero regardless of shaft movement
- Count jumps erratically or bounces
- Count only increases, never decreases (or vice versa)
- Position drifts over time even without movement
- Encoder count is much lower than expected
- Intermittent signal dropout
- Encoder works at slow speed but loses counts at high speed

## Likely Causes
- Zero reading → no power, broken wire, blocked optical disk
- Erratic count → electrical noise, loose mounting, signal wire near motor wire
- One direction only → one channel wire (A or B) broken or disconnected
- Position drift → noise triggering false counts, insufficient signal filtering
- Low count → encoder resolution mismatch in firmware
- Dropout → loose connector, intermittent wire break
- Loses counts at speed → signal frequency exceeds microcontroller interrupt rate

## Safe First Checks
- Check encoder supply voltage (typically 3.3V or 5V)
- Wiggle encoder connector — watch if any count changes occur (indicates loose connection)
- Confirm A, B, and GND wires all have continuity back to controller
- For optical encoders: check if encoder disk is clean and not blocked by debris
- Verify encoder cable is routed away from motor power cables

## Tools Needed
- Multimeter
- Oscilloscope or logic analyzer (recommended)
- Contact cleaner spray (for optical disk)
- Cable tie or cable management clips

## Step-by-Step Guidance
1. Power on system. Slowly rotate encoder shaft by hand. Count should increment smoothly.
2. If count stays zero → measure supply voltage at encoder. If missing → check wiring.
3. If supply OK but no count → swap encoder if possible to rule out dead encoder vs. wiring fault.
4. If count only goes one direction → disconnect channel A wire, then B wire one at a time. Whichever removal stops all counts is the working channel. Other channel is broken.
5. For erratic counts → route signal wires in separate cable bundle from motor power wires. Add 100nF capacitor between each signal line and GND near controller.
6. For optical encoder → remove disk cover (if accessible without disassembly) and spray with contact cleaner. Dry completely before powering on.
7. For count mismatch → verify encoder CPR (counts per revolution) matches firmware configuration. CPR × 4 = PPR for quadrature.
8. For high-speed dropout → ensure microcontroller is using hardware interrupts, not software polling. Reduce max speed or use encoder with lower CPR.
9. Check encoder mounting screws — loose encoder housing shifts disk alignment and causes miss-counts.
10. If all checks pass but problem persists → replace encoder.

## Stop Conditions
- **STOP** if encoder supply voltage exceeds maximum — most encoders are 5V max, 3.3V models damaged by 5V
- **STOP** if encoder cable insulation is damaged near motor — risk of short circuit to high-current motor wiring
- Do not attempt to open sealed magnetic or Hall-effect encoders — factory-calibrated

## Prevention
- Always separate encoder signal cables from motor power cables
- Use shielded twisted-pair cable for encoder signals on cables longer than 30cm
- Secure encoder mounting rigidly — vibration causes alignment drift
- Add hardware debounce or use encoder library with filtering
- Label encoder CPR spec on robot for future reference

## Keywords
- encoder not reading, encoder count wrong, quadrature encoder fault, Hall effect encoder
- encoder drift, encoder noise, encoder dropout, encoder interrupt, CPR PPR resolution
- optical encoder, magnetic encoder, encoder A B channel, encoder wiring
- encoder troubleshooting, position feedback fault, encoder losing counts
