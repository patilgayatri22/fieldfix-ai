# Electronic Sensors — Repair Guide (Temp / Humidity / IMU / Accelerometer)

## Common Symptoms
- Sensor returns constant fixed value (e.g., always 0 or always max)
- Sensor reads wildly incorrect values (100°C room temperature)
- Sensor worked then stopped after touching wires
- Humidity sensor reads 0% or 100% regardless of environment
- IMU / accelerometer reads constant tilt even when flat
- Sensor values drift over time
- Sensor stops responding after power cycle
- Two sensors of same type give very different readings

## Likely Causes
- Constant value → sensor not responding to I2C/SPI (check address and comms), supply issue
- Wildly wrong → library reading wrong register, incorrect conversion formula in code, sensor overloaded
- Stopped after touching → ESD damage from handling without grounding, wire pulled loose
- Humidity always extreme → sensor element contaminated, condensation damage, sensor expired
- IMU constant tilt → calibration offsets not applied, sensor mounted at angle
- Drift over time → temperature coefficient, self-heating, insufficient settling time after power on
- Stops after power cycle → I2C address conflict introduced, brownout corrupted sensor config register
- Two sensors differ → manufacturing tolerance (normal within spec), one sensor damaged

## Safe First Checks
- Run I2C scanner to confirm sensor is detected at expected address
- Check supply voltage at sensor VCC — match to rated voltage (3.3V or 5V)
- Check sensor is not near heat source, fan, or direct draft that could bias reading
- For DHT11/DHT22: ensure data pin has 4.7kΩ–10kΩ pull-up resistor
- For IMU: keep flat on table, read values — should show near-zero roll and pitch, ~1g on Z axis

## Tools Needed
- Multimeter
- Microcontroller with serial monitor
- Anti-static wrist strap (for handling bare sensor PCBs)

## Step-by-Step Guidance
1. Verify sensor detected: run I2C scanner. DHT sensors: verify data wire pull-up exists and timing library is correct.
2. Read raw register values (not library-processed). If raw data is all zeros → sensor not communicating. Check wiring and supply.
3. For temp/humidity sensor returning impossible values → verify you're using correct library for specific variant: DHT11 ≠ DHT22. Pins differ.
4. For DHT sensor "failed to read" → check pull-up resistor on data line. Increase pull-up to 4.7kΩ if missing. Keep wire under 20cm.
5. For IMU (MPU6050, ICM42688, etc.) giving wrong orientation → apply calibration. Most libraries have calibration methods. Place sensor flat, run calibration, store offsets in code.
6. For drifting values → allow 2-second warm-up time after power on before reading. If drift continues across minutes → check for self-heating from nearby components.
7. For humidity sensor at 0% or 100% → inspect sensor element visually. Condensation or liquid contact permanently degrades DHT11/DHT22 elements. Replace sensor.
8. For sensor stopping after power cycle → add I2C bus reset (9 clock pulses) in setup() before sensor initialization.
9. For two sensors reading differently → check if both are within tolerance spec (DHT11 ±2°C, DHT22 ±0.5°C, MPU6050 ±0.5°C). If one is far outside spec → that sensor is damaged.
10. For ESD-damaged sensor → replace. ESD damage is not repairable. Use anti-static precautions in future handling.

## Stop Conditions
- **STOP** if applying 5V to 3.3V sensor — permanent damage
- **STOP** if sensor is in condensing moisture environment — water ingress damages most sensors
- Do not expose bare BME280/BMP280 sensors to high humidity without protective coating

## Prevention
- Handle all sensor PCBs with anti-static mat or wrist strap
- Allow 2-second initialization time in code before first reading
- Mount temperature sensors away from heat sources (regulators, power resistors)
- Protect humidity sensors with breathable membrane covers
- Re-run IMU calibration if sensor is moved or remounted

## Keywords
- temperature sensor wrong reading, DHT11 not working, DHT22 failed, humidity sensor fault
- MPU6050 not reading, IMU calibration, accelerometer always tilted, IMU drift
- BMP280 fault, BME280 not detected, sensor returns zero, sensor I2C address
- electronic sensor troubleshooting, sensor ESD damage, sensor pull-up resistor, sensor warm-up time
