# Robotic Power System — Repair Guide (Battery Packs / BEC / Voltage Regulators)

## Common Symptoms
- Robot resets or reboots under load
- Battery drains unusually fast
- Voltage regulator output lower than rated
- Components behave erratically near full battery drain
- BEC (Battery Eliminator Circuit) gets very hot
- Battery pack swells, feels puffy, or leaks
- Robot shuts down immediately after powering on
- Motors run but logic board resets repeatedly

## Likely Causes
- Resets under load → voltage sag, undersized wiring, failing battery
- Fast drain → internal short, parasitic load, incorrect battery capacity for task
- Low regulator output → overloaded regulator, poor input voltage, failing regulator IC
- Erratic behavior near empty → battery voltage cutoff needed, brown-out protection
- Hot BEC → overloaded BEC current rating
- Swollen/leaking battery → overcharge, over-discharge, internal cell failure — SAFETY ISSUE
- Immediate shutdown → battery protection circuit tripping, dead cell in pack
- Logic resets during motor move → servo/motor and logic share power, insufficient decoupling

## Safe First Checks
- Measure battery voltage at rest (no load) — should be within 0.2V of rated full charge
- Measure battery voltage under load — sag more than 1V indicates weak battery
- Check wiring gauge — thin wires cause high resistance and voltage drop
- Check connector condition — corrosion or poor crimp causes voltage drop
- Look at battery pack — any bulging, puffiness, or deformation is a STOP condition
- Check regulator output voltage with multimeter

## Tools Needed
- Multimeter
- Battery capacity tester (optional)
- Fuse holder and appropriate fuse
- Heat shrink tubing

## Step-by-Step Guidance
1. Measure battery voltage open-circuit. LiPo full = 4.2V/cell, nominal = 3.7V/cell, cutoff = 3.0V/cell. NiMH full = 1.4V/cell, cutoff = 1.0V/cell.
2. Connect load and re-measure. Voltage should not drop more than 0.5V (good battery). Drop > 1V = replace battery.
3. Measure voltage at regulator input and output. Input must be at least 1.5V above output (linear regulators) or within switching regulator input range.
4. If regulator output is low → check output current draw with multimeter in series. If exceeds regulator rating → add second regulator or upgrade.
5. For logic resets during motor movement → add 1000µF capacitor across logic supply rails near main controller. Separate motor and logic power rails if possible.
6. For hot BEC → calculate total servo/logic current. If within 80% of BEC rating, add heatsink. If over rating, upgrade BEC.
7. Check all main power connectors (XT30, XT60, Deans, barrel jack) for burn marks or looseness. Loose power connectors under high current cause arcing.
8. Ensure main power circuit has a fuse rated at 110% of maximum expected current.
9. For fast battery drain → identify all loads, sum current draw. Compare to battery capacity. Increase capacity or reduce loads.
10. For battery that dies immediately → test each cell voltage individually if accessible. Dead cell = replace pack.

## Stop Conditions
- **STOP** if battery is swollen, puffy, or leaking — do not charge or discharge, place in fireproof container, dispose properly
- **STOP** if battery connector is sparking during connection — indicates short circuit or reverse polarity
- **STOP** if any wire is hot to touch during operation — wire gauge too small, fire risk
- **STOP** if regulator smells like burning — disconnect power immediately
- Never charge LiPo batteries unattended or without a LiPo-rated charger

## Prevention
- Always add a low-voltage cutoff circuit to protect LiPo cells from over-discharge
- Size wiring to carry 2× expected current — prevents heating
- Use XT60 or XT30 connectors for high-current paths — avoid barrel jacks above 5A
- Balance-charge LiPo packs every cycle
- Store LiPo at storage voltage (3.8V/cell) if not using for more than a week

## Keywords
- robot power supply, voltage sag, battery drain, BEC fault, LiPo battery
- voltage regulator failing, brown-out reset, robot rebooting under load
- battery pack dead, swollen battery, NiMH robot battery, XT60 connector
- robot power troubleshooting, logic reset during motor, low voltage cutoff, battery cell dead
