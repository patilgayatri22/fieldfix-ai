# Soldering & PCB — Repair Guide (Cold Joints / Shorts / Lifted Pads)

## Common Symptoms
- Component works intermittently — wiggles in/out of function
- Device fails after heat cycling (works when cold, fails when warm)
- Continuity test fails between component pin and trace
- Visible dull, grey, or cracked solder joint
- Two adjacent pads have unintended electrical connection (solder bridge)
- Component pin lifts off PCB when touched
- Pad came off board entirely
- Device partially works — some functions fine, others dead

## Likely Causes
- Intermittent function → cold solder joint (insufficient heat during soldering)
- Heat-dependent failure → cracked joint expands/contracts with temperature
- Continuity failure → cold joint, lifted pad, or broken trace
- Dull grey joint → cold joint — not enough heat, joint moved while cooling
- Solder bridge → too much solder, poor soldering technique
- Lifted pin → overheated joint, mechanical stress on component
- Pad lifted → excessive heat or mechanical force during rework
- Partial function → affected signal path identifies which pad/component is failed

## Safe First Checks
- Inspect all solder joints under good lighting or magnification — look for dull, cracked, or incomplete joints
- Gently press each component with a wooden/plastic tool while system is running — intermittent fault locates itself
- Check for visible solder bridges between adjacent pins with magnifying glass
- Test continuity with multimeter between suspicious pin and its trace
- Check for flux residue — can cause leakage current between pads (clean with isopropyl alcohol)

## Tools Needed
- Soldering iron (temperature-controlled preferred)
- Solder (rosin-core, 60/40 or lead-free)
- Flux pen or flux paste
- Solder wick (desoldering braid)
- Magnifying glass or loupe
- Isopropyl alcohol (90%+) and cotton swabs
- Multimeter

## Step-by-Step Guidance
1. Inspect all joints with magnification. A good joint is shiny (or matte for lead-free), smooth, volcano-shaped. A bad joint is dull, grey, lumpy, or has visible cracks.
2. To reflow cold joint: apply flux, touch iron tip to joint for 3–5 seconds. Joint should reflow and settle. Remove iron. Do not move for 5 seconds while cooling.
3. For solder bridge: apply flux to bridged area. Drag soldering iron tip from one side across the bridge — it usually follows the iron. If not, use solder wick.
4. For solder wick: press braid onto solder bridge with iron tip. Wick absorbs solder. Move to fresh wick section when saturated. Wick must be pre-tinned for best results.
5. For broken trace: scrape 1–2mm of solder mask away from each end of break using sharp blade (gently). Apply flux and solder a short bridge wire across the break.
6. For lifted pad → do NOT try to resolder the pad back down. Bridge the connection: use a thin magnet wire from the component lead to the nearest via or trace endpoint that connects to that net.
7. After all rework: clean board with isopropyl alcohol and cotton swab to remove flux residue.
8. Re-test continuity between all reworked joints and their destination traces.
9. Power on and test full functionality. Heat-cycle (power on/off 3 times) to confirm no heat-dependent failures remain.
10. If pad is gone entirely → use the component's datasheet to trace net to another via or test point on the board and jumper there.

## Stop Conditions
- **STOP** soldering if iron temperature is unknown — working on sensitive SMD components above 380°C damages them
- **STOP** if PCB starts to delaminate (layers separating, surface bubbling) — excessive heat is destroying the board
- **STOP** if you see a visible crack in the PCB substrate — structural integrity compromised
- Never use acid-core solder on electronics — only rosin/flux-core

## Prevention
- Use flux on every joint — it prevents cold joints and makes rework easy
- Keep iron tip clean and tinned — oxidized tip transfers heat poorly
- Solder at correct temperature: 320–350°C for leaded, 350–380°C for lead-free
- Avoid mechanical stress on solder joints — strain relief all wires
- Inspect boards under magnification after soldering before first power-on

## Keywords
- cold solder joint, solder bridge, PCB repair, lifted pad, broken trace
- solder wick, desoldering, flux, intermittent connection, continuity test
- PCB troubleshooting, SMD rework, through-hole soldering, bad solder joint
- component intermittent, heat-dependent fault, PCB bridging, trace repair
