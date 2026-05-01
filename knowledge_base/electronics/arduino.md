# Arduino — Repair Guide (Uno / Nano / Mega / Leonardo)

## Common Symptoms
- Upload fails with "avrdude: stk500_recv() error" or similar
- Sketch uploads but does nothing
- Serial monitor shows garbage characters
- Components connected to pins don't respond
- Arduino resets randomly during operation
- Power LED on but board appears dead
- Board gets warm/hot during operation
- Sketch runs once then stops

## Likely Causes
- Upload error → wrong board/port selected, CH340/FTDI driver missing (Nano clone), bootloader corrupted
- Uploads but nothing happens → wrong pin numbers in code, logic error, component wiring fault
- Serial garbage → wrong baud rate in Serial Monitor, not matching Serial.begin() rate
- Pins not responding → wrong pin mode (not set as OUTPUT), pins in use by other hardware (SPI, I2C, UART)
- Random resets → power supply noise, watchdog timer in sketch, brown-out
- Dead board → fuse settings wrong after ISP programming, linear regulator failed
- Overheating → onboard 5V regulator overloaded, too much current drawn from pins
- Runs once then stops → blocking code (while loop without exit), sketch logic issue

## Safe First Checks
- Check IDE has correct Board and Port selected (Tools menu)
- Try different USB cable — many USB cables are charge-only with no data wires
- Check USB port on computer — try different port or computer
- Verify RX/TX LEDs blink briefly during upload attempt
- Check 5V and GND rails are connected correctly to components
- Measure 5V pin with multimeter — should be 4.8V–5.2V

## Tools Needed
- Multimeter
- Arduino IDE (or PlatformIO)
- USB cable (data-capable)
- Second Arduino (for bootloader reflash, if needed)

## Step-by-Step Guidance
1. Open Arduino IDE. Tools > Board: select correct model. Tools > Port: select correct COM/dev port.
2. Upload minimal sketch (Blink). If this fails → driver or hardware issue.
3. For upload error on Nano clone → Tools > Processor: select "ATmega328P (Old Bootloader)". Most cheap Nano clones use old bootloader.
4. If still fails → check CH340 driver installed (Windows: Device Manager, look for "USB-SERIAL CH340"). Install from CH340 driver package.
5. If Blink uploads but LED doesn't blink → verify LED is on pin 13 (or check which pin has built-in LED for your board).
6. For serial garbage → match baud rate: Serial.begin(9600) in sketch must equal 9600 in Serial Monitor dropdown.
7. For components not responding → check wiring continuity. Verify pin mode: `pinMode(pin, OUTPUT)` before `digitalWrite()`. Verify pin numbers match physical labels on board.
8. For random resets → check 5V supply under load. Add 100µF capacitor on 5V rail. Check sketch for watchdog timer (`wdt_enable()`).
9. For overheating onboard regulator → check total current drawn from 5V and 3.3V pins. Max from pins = 200mA (Uno). Offload high-current loads to external supply.
10. For board that won't upload at all after ISP programming → reflash bootloader via ISP with second Arduino using Arduino IDE (Tools > Burn Bootloader).

## Stop Conditions
- **STOP** if Arduino is hot to touch — disconnect, find overcurrent source
- **STOP** if pin voltage exceeds 5V input — voltage above 5V on analog or digital pins damages ATmega
- **STOP** if board smells like burning — IC damage, do not power again
- Do not draw more than 40mA from any single digital pin — use transistor/MOSFET for higher loads

## Prevention
- Always use DATA-capable USB cable — test with a known-working cable
- Keep a known-working "Blink" sketch to quickly test board health
- Add series resistors (220Ω–1kΩ) on any pin driving LEDs or transistors
- Power high-current loads (servos, motors) from external supply, not Arduino pins
- Install CH340 driver on every development machine before use

## Keywords
- Arduino upload error, avrdude error, Arduino not uploading, Arduino sketch not running
- serial garbage characters, wrong baud rate, Arduino pin not working, Arduino resets
- CH340 driver, FTDI driver, Arduino Nano clone, bootloader corrupt, Blink not working
- Arduino overheating, Arduino troubleshooting, ATmega328 fault, Arduino dead board
