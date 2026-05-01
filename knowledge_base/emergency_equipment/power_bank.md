# Power Bank — Repair Guide (Portable Battery Pack)

## Common Symptoms
- Power bank won't charge connected device
- Power bank doesn't charge (no LED activity when plugged in)
- Charges device very slowly
- Shows full charge but dies after a few minutes
- Won't turn on after sitting unused for months
- Overheats during charging or discharging
- USB port wobbles or cable won't seat properly
- Shows full LEDs but device shows no charging

## Likely Causes
- Won't charge device → output triggered by device but current too low, sleep mode (low-draw devices), output port damage
- Won't charge itself → cable fault, input port damage, battery fully discharged (below recovery threshold)
- Slow charging → cable quality, adapter output too low, both charging simultaneously, thermal throttling
- Shows full but dies quickly → battery cells have degraded, capacity loss after many cycles
- Won't turn on after storage → battery over-discharged below recovery threshold (lithium batteries die if left at 0%)
- Overheating → simultaneous charge/discharge, inadequate ventilation, cell failure
- Loose USB port → physical damage, repeated connector stress, soldering failed internally
- Full LEDs but no output on device → device connection fault, cable fault, output port fault

## Safe First Checks
- Try a different USB cable — most charging issues are cable faults not power bank faults
- Try a different device to test output
- Check USB input cable and adapter — use adapter rated at same wattage as power bank input spec
- Check battery indicator LEDs — press power button to check charge state
- Feel temperature — should be warm, not hot, during charging

## Tools Needed
- Multimeter (USB voltage tester optional)
- Multiple known-good USB cables
- USB charger rated for power bank's input spec (usually 5V/2A minimum)

## Step-by-Step Guidance
1. Try a different cable — rule out cable fault first.
2. If power bank won't turn on at all → connect to charger for 30 minutes before testing. Deeply discharged banks need trickle charge recovery time.
3. If no charging LED after 30 minutes → try different charger and cable combination. Some banks are picky about input voltage.
4. For sleep mode issue (can't charge low-draw device like earbuds) → press power button to manually activate output. Some banks have auto-off below a current threshold.
5. For slow output → check adapter rating. A 5W (5V/1A) phone charger limits input to 5W even if power bank can accept 18W. Match adapter wattage to power bank spec.
6. For reduced capacity → this is normal degradation. Lithium cells lose 20% capacity after ~300 cycles. If capacity has dropped dramatically → power bank is at end of life.
7. For overheating → stop charging immediately. Allow to cool in open air. Do not cover or enclose while charging. Check if simultaneous charge+discharge is happening (daisy-chain charging).
8. For wobbly USB port → this is internal connector damage. Do not force cables. Attempting repair requires soldering — not field-repairable without tools and skill.
9. For power bank that died after long storage → attempt recovery: connect to charger, wait 1 hour. If no response → cells may be unrecoverable. Do not attempt to force-charge a dead lithium cell.
10. If power bank is swollen, hot without use, or deformed → see battery_safety.md immediately.

## Stop Conditions
- **STOP** if power bank is swollen or puffy — lithium cells are venting, fire hazard — remove from bag/pocket, place in open area away from flammables
- **STOP** if power bank is hot without being used — thermal runaway risk
- **STOP** if power bank produces hissing, crackling, or burning smell — place outside immediately
- Never puncture, crush, or disassemble a lithium power bank
- Do not store in hot car or direct sunlight for extended periods

## Prevention
- Store power bank at 40–80% charge if not using for extended periods — full or empty storage degrades cells faster
- Use quality cables with proper rating — cheap cables cause slow charge and heat
- Do not leave fully charged power bank on charge indefinitely (overcharge stresses cells)
- Inspect USB ports regularly for damage — cable strain is the most common physical failure
- Charge in a cool, ventilated location — not under pillows or in enclosed bags

## Keywords
- power bank not working, power bank won't charge, portable charger dead, power bank slow charging
- power bank capacity loss, power bank overheating, USB port broken, power bank swollen
- power bank won't turn on, power bank sleep mode, portable battery pack repair
- power bank cable fault, power bank deep discharge recovery, lithium battery pack
