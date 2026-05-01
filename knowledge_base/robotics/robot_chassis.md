# Robot Chassis — Repair Guide (Wheels / Frame / Drive Train)

## Common Symptoms
- Robot drives in a curve instead of straight
- Wheels slip on smooth surfaces
- Frame vibrates heavily at speed
- Robot can't climb small inclines it previously managed
- One wheel spins, other doesn't (differential drive)
- Wheel wobbles side to side during rotation
- Robot makes scraping noise from underneath
- Chassis flexes noticeably when turning

## Likely Causes
- Curves instead of straight → wheel diameter mismatch, motor speed imbalance, encoder calibration off
- Wheel slip → tire compound worn/dirty, wheel too smooth for surface, insufficient weight/traction
- Heavy vibration → wheel out of balance, bent axle, loose wheel hub
- Can't climb inclines → motors under-torqued, battery voltage sagging under load
- One wheel not driving → motor/driver fault on that channel, wiring break, wheel coupler slip
- Wheel wobbles → loose hub set screw, bent axle, improper wheel press fit
- Scraping noise → cable or component dragging, wheel misaligned inward
- Chassis flex → frame cracked, structural fasteners loose, unsupported spans too long

## Safe First Checks
- Spin each wheel by hand — should be smooth, equal resistance on both sides
- Check all wheel hub set screws — Allen key, should be tight
- Inspect chassis underside for dragging wires or components
- Check motor mount screws — vibration loosens these over time
- Drive robot slowly on flat surface and observe direction consistency
- Flex chassis gently by hand — any cracking sounds indicate structural issue

## Tools Needed
- Allen/hex key set
- Screwdrivers
- Ruler or calipers (wheel diameter check)
- Contact cleaner or isopropyl alcohol (tire cleaning)

## Step-by-Step Guidance
1. Power off. Remove wheels one at a time. Check each wheel for flat spots, wear, or dirt buildup on tire surface.
2. Clean tires with isopropyl alcohol wipe. Rough up slightly with sandpaper if too smooth. Retest traction.
3. Measure diameter of left and right wheels with calipers. Mismatch > 0.5mm can cause consistent curve. Swap matched-diameter wheels if available.
4. Tighten all wheel hub set screws. Confirm wheel is fully seated against hub shoulder — no axial gap.
5. Check motor mount fasteners. Tighten all. If threads stripped → add thread insert or move to adjacent hole.
6. For one-wheel fault → test that motor/driver in isolation (see dc_motor.md, motor_driver.md).
7. For persistent straight-line drift → calibrate encoder counts per revolution for both wheels. Adjust speed scaling in firmware for left/right to match.
8. For vibration at speed → lift robot off ground. Spin each wheel with motor. Vibration at speed = wheel imbalance or bent axle. Replace affected wheel/axle.
9. For scraping noise → run robot slowly and look under chassis. Identify contact point. Re-route cables or add clearance.
10. For chassis flex → reinforce with additional structural members or gussets. Tighten all structural fasteners. Replace cracked frame sections.

## Stop Conditions
- **STOP** if chassis crack is visible in load-bearing section — risk of collapse
- **STOP** if wheel comes off during operation — motor shaft exposed and spinning
- **STOP** if dragging wire is near motor drive belt or chain — entanglement risk
- Do not operate robot on wet or conductive surfaces without verified waterproofing

## Prevention
- Degrease and inspect tires before each competition or extended run session
- Apply threadlocker to all chassis structural fasteners
- Route cables through dedicated cable channels, never loose under chassis
- Check wheel set screws weekly during heavy-use periods
- Design chassis with redundant fastening at high-stress joints

## Keywords
- robot drives in curve, wheel slip, robot vibration, chassis flex, wheel wobble
- motor speed mismatch, wheel hub loose, axle bent, drive train fault
- robot traction, differential drive problem, robot not going straight
- robot chassis troubleshooting, wheel alignment, one wheel not working, encoder wheel calibration
