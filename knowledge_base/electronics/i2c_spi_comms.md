# I2C / SPI Communication — Repair Guide

## Common Symptoms
- I2C device not detected (address scan returns nothing)
- I2C communication errors or corrupted data
- SPI device returns 0x00 or 0xFF for all reads
- I2C bus hangs/freezes entire system
- Only first device works in multi-device chain
- SPI works at low speed but fails at higher clock
- I2C works at short cable, fails at longer cable
- Intermittent communication errors

## Likely Causes
- I2C device not found → wrong address, missing pull-up resistors, device not powered, wrong SDA/SCL pins
- Corrupted data → no pull-up resistors, excessive capacitance on bus, noise
- SPI returns 0x00/0xFF → chip select (CS) not toggling, MISO/MOSI swapped, SPI mode wrong
- I2C bus hang → device holding SDA low after interrupted transaction, no timeout in firmware
- Multi-device failure → address conflict, pull-up resistors too weak for multiple devices
- High-speed SPI failure → cable too long, no series termination resistor, timing margin exceeded
- Long cable failure → I2C bus capacitance too high, reduce pull-up value (2.2kΩ instead of 10kΩ)
- Intermittent errors → loose connection, interference, voltage level mismatch (3.3V vs 5V)

## Safe First Checks
- Verify SDA and SCL (I2C) or MOSI/MISO/SCK/CS (SPI) wiring matches microcontroller pinout
- Confirm device supply voltage (3.3V or 5V) matches device spec
- For I2C: confirm pull-up resistors exist on SDA and SCL lines (typically 4.7kΩ to supply)
- Check for address conflicts: two I2C devices with same address on one bus = both broken
- Verify logic levels match: 5V microcontroller + 3.3V device needs level shifter

## Tools Needed
- Multimeter
- Logic analyzer (strongly recommended)
- Pull-up resistors (4.7kΩ, 2.2kΩ)
- Level shifter module (if mixing 3.3V and 5V)

## Step-by-Step Guidance
1. Run I2C scanner sketch to list all detected addresses. If empty → wiring or power issue.
2. Measure SDA and SCL with multimeter (no transaction running) — both should be HIGH (pulled to supply voltage).
3. If either line is LOW at rest → I2C bus is hung. Power cycle all devices. If persistent → one device holds bus low after failed transaction. Add I2C bus reset in firmware (toggle SCL 9 times).
4. If address scan finds nothing → check pull-up resistors present (4.7kΩ from SDA to VCC, SCL to VCC). Without them, I2C doesn't work.
5. If address found but data wrong → verify I2C clock speed. Default 100kHz works for all devices. Some modules (especially OLED) struggle above 400kHz.
6. For SPI issues → check CS pin is toggling (goes LOW before transaction, HIGH after). Use logic analyzer to verify MOSI, MISO, SCK waveforms.
7. For SPI returning 0xFF → MISO line is floating high. Verify MISO connected to correct pin. Some devices need CS to go low first before MISO becomes active.
8. For 3.3V/5V mismatch → add bidirectional level shifter (e.g., BSS138-based module) on SDA/SCL for I2C, or all data lines for SPI.
9. For long cable I2C failure → reduce pull-up resistor value to 2.2kΩ or 1kΩ to drive higher cable capacitance.
10. For multi-device SPI → each device must have its own unique CS pin. Never share CS lines.

## Stop Conditions
- **STOP** if connecting 5V I2C/SPI signals to 3.3V device without level shifter — permanent damage
- **STOP** if bus is stuck and power cycling doesn't clear it — investigate firmware before continuing
- Do not run I2C at >400kHz without confirming all devices support Fast Mode

## Prevention
- Always include pull-up resistors in I2C circuit design — don't rely on internal weak pull-ups alone
- Use unique I2C addresses — check all device addresses before combining on one bus
- Keep I2C wire length under 30cm for reliable operation without tuning
- Add I2C bus timeout and recovery code to handle bus hangs gracefully
- Use SPI for high-speed or long-distance communication — it's more robust than I2C

## Keywords
- I2C device not found, I2C address scan empty, I2C bus hang, I2C pull-up resistors
- SPI not working, SPI returns 0xFF, chip select CS pin, MOSI MISO SCK wiring
- I2C address conflict, level shifter 3.3V 5V, I2C long cable, SPI mode wrong
- I2C communication error, SPI communication fault, I2C troubleshooting, SPI troubleshooting
