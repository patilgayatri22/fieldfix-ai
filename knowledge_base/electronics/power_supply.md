# Power Supply — Repair Guide (Bench PSU / Switching / Linear Regulators)

## Common Symptoms
- Output voltage lower than set or rated value
- Output voltage unstable or rippling
- Power supply shuts off under load
- Output noisy — components behave erratically
- Regulator module very hot
- Output correct at no load but drops under load
- Fuse blows repeatedly
- Power supply output correct but circuit doesn't work

## Likely Causes
- Low output → overloaded beyond current rating, failing regulator, poor input voltage
- Unstable output → output capacitor dried out or missing, load too dynamic
- Shuts off under load → over-current protection triggered, thermal shutdown
- Noisy output → insufficient output capacitor, no bulk capacitor, switching frequency interference
- Hot regulator → linear regulator dissipating (Vin-Vout) × Iout as heat — normal but may need heatsink
- Voltage drop under load → wiring resistance, connector resistance, weak supply
- Fuse blows → short circuit in load, fuse undersized, load current spike
- Circuit doesn't work despite correct voltage → wrong polarity, ground not connected properly

## Safe First Checks
- Measure output voltage with multimeter under load and at no load
- Check input voltage is within regulator's rated input range
- Feel regulator body after 30 seconds under load — warm is normal, hot requires heatsink
- Check for loose or corroded connections at output terminals
- Verify polarity is correct (positive/negative) before connecting
- Check wiring gauge is sufficient for current (too thin = high resistance = voltage drop)

## Tools Needed
- Multimeter
- Oscilloscope (for ripple/noise measurement, optional)
- Heatsink and thermal paste
- Known-load resistor (for testing PSU under controlled load)

## Step-by-Step Guidance
1. Measure output voltage with no load connected. Should match rated or set value ±2%.
2. Connect a known resistor load (calculate R = V/I for desired test current). Re-measure output.
3. If voltage drops more than 5% under load → supply is overloaded or has high output impedance.
4. For linear regulator (7805, LM317, AMS1117) getting hot → calculate heat: P = (Vin - Vout) × Iout. If P > 500mW → attach heatsink. If P > 1W → switch to switching regulator.
5. For switching regulator with noisy output → add 100µF electrolytic + 100nF ceramic capacitor at output. Check if minimum load is required (some switching regs need minimum load to regulate).
6. For voltage collapse under dynamic load (motors starting) → add large bulk capacitor (470µF–2200µF) at power rail near load.
7. For blown fuse → disconnect all loads. Power on with no load. If fuse holds → add loads one by one to find the short circuit.
8. For thermal shutdown → check regulator's maximum junction temperature spec. Add heatsink, improve airflow, or reduce load.
9. For output correct but circuit not working → verify GND is connected between power supply and circuit (common ground). Check polarity.
10. For persistent underpowering → upgrade to higher-current rated supply or regulator.

## Stop Conditions
- **STOP** if any component produces burning smell or visible smoke — disconnect immediately
- **STOP** if output voltage is significantly above rated (overvoltage) — can destroy downstream components
- **STOP** if fuse blows immediately on power-on with no load — indicates internal short in power supply
- Never bypass a blown fuse with wire — it exists to prevent fire and component damage
- Do not exceed regulator input voltage maximum — common mistake destroys IC instantly

## Prevention
- Size power supply at 125–150% of maximum expected load current
- Use switching regulators for any input/output differential > 3V to avoid excessive heat
- Add decoupling capacitors at every IC's power pin in the circuit
- Use a fuse rated just above maximum normal operating current
- Label polarity on all custom power cables and connectors

## Keywords
- power supply voltage drop, voltage regulator fault, linear regulator hot, switching regulator noise
- LM7805 fault, AMS1117 fault, LM317 adjustment, PSU overload, voltage collapse under load
- power supply shutting off, fuse blowing, ripple noise, bulk capacitor, power supply troubleshooting
- output voltage low, voltage sag, power rail unstable, common ground missing
