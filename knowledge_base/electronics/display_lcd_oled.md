# LCD / OLED Display — Repair Guide

## Common Symptoms
- Display shows nothing (completely blank)
- Display shows blocks or rectangles, no characters
- Display has correct backlight but no text
- OLED shows garbled or partial output
- Display worked once, now shows random characters
- Text is very faint or barely visible
- I2C OLED not detected at expected address
- Display flickers or goes blank intermittently

## Likely Causes
- Completely blank → no power, contrast too low (LCD), I2C address wrong (OLED)
- Blocks only → LCD initialized but no contrast voltage — adjust contrast pot
- Backlight on, no text → LCD not initialized in code, wrong library or pin assignment
- OLED garbled → I2C data corruption, incorrect display dimensions in library init
- Worked once now garbage → loose wire, library not matching hardware variant
- Faint text → LCD contrast pot set too high (counterintuitively, turn it)
- I2C OLED not found → common addresses are 0x3C and 0x3D — try both
- Flickering → loose power connection, insufficient supply current, software update rate too high

## Safe First Checks
- For LCD: locate the small potentiometer (blue trim pot) on backpack/module — turn it slowly
- Check supply voltage at display VCC pin — 5V for most LCDs, 3.3V for most OLEDs
- For I2C displays: run I2C scanner to confirm address detected
- Check all wires — SDA, SCL, VCC, GND, and for parallel LCD: all data bus pins
- For character LCD: confirm cursor character appears in top-left when uninitialized (indicates LCD alive)

## Tools Needed
- Multimeter
- Small flat-head screwdriver (for contrast pot)
- I2C scanner sketch

## Step-by-Step Guidance
1. Verify power: measure VCC and GND pins at display. Correct voltage must be present.
2. For character LCD with I2C backpack: run I2C scanner. Common backpack addresses: 0x27 (PCF8574), 0x3F (PCF8574A). If no address found → check pull-ups and wiring.
3. If I2C address found but nothing on screen → adjust contrast potentiometer. Turn slowly — it's very sensitive. Correct position shows solid blocks (contrast too high) transitioning to faint text (correct).
4. For parallel LCD (without I2C): verify RS, EN, D4, D5, D6, D7 wires match pin assignment in code. One wrong wire = garbage or nothing.
5. If display shows startup text then freezes → check if display is sharing I2C bus with another device. Try running display alone.
6. For OLED (SSD1306): in library initialization, confirm width (128) and height (32 or 64) match physical display. Wrong height = partial or garbled output.
7. For OLED at wrong address: most common addresses are 0x3C and 0x3D. If your library specifies one but hardware uses other → change in begin() call: `display.begin(SSD1306_SWITCHCAPVCC, 0x3C)`.
8. For flickering → check VCC current draw vs supply capacity. OLED draws up to 30mA. LCD + backlight up to 60mA. Ensure supply can handle this.
9. For faint text → on parallel LCD, increase contrast (turn pot in small increments). On OLED, increase contrast in software: `display.setContrast(255)`.
10. If display works in test sketch but not application → application may be sending wrong data or clearing screen too frequently. Add delay between display updates.

## Stop Conditions
- **STOP** if applying 5V to a 3.3V OLED — permanent damage (check spec before powering)
- **STOP** if display produces burning smell — disconnect, likely dead from incorrect voltage
- Do not force contrast pot beyond its mechanical limits

## Prevention
- Confirm voltage rating before first connection — many OLEDs are 3.3V only
- Use I2C scanner to find correct address before writing initialization code
- For character LCDs, write contrast pot position on a label once found — saves re-tuning after disconnect
- Add bulk capacitor (100µF) on display VCC pin to prevent flicker from current spikes
- Keep display refresh rate under 30fps — rapid updates cause I2C bus congestion

## Keywords
- LCD blank, LCD no display, LCD blocks only, LCD contrast adjustment, LCD backlight on no text
- OLED not working, OLED garbled, SSD1306 address, I2C OLED not detected
- LCD I2C backpack, PCF8574 address, display flickers, OLED faint, LCD faint text
- display troubleshooting, LCD repair, OLED repair, character LCD parallel wiring
