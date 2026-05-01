# Raspberry Pi — Repair Guide (All Models)

## Common Symptoms
- Pi shows no video output on boot
- Red power LED flashes or turns off during boot
- Pi boots to rainbow screen and stops
- Pi boots but then freezes or crashes randomly
- GPIO pins not working as expected
- Pi overheats and throttles
- SSH not accessible after power cycle
- SD card not detected or corrupted filesystem

## Likely Causes
- No video → HDMI not plugged before power-on (older Pi), wrong display config, damaged HDMI port
- Power LED flashing/off → undervoltage, bad power supply, high current load
- Rainbow screen freeze → corrupted or incompatible SD card image, bad SD card
- Random freezes → undervoltage, overheating, corrupted OS, bad RAM
- GPIO not working → wrong pin numbering (BCM vs BOARD), pin already in use by kernel, insufficient drive current
- Overheating → no heatsink, poor airflow, overclocking without cooling
- SSH inaccessible → hostname resolution issue, DHCP lease change, SSH disabled in image
- SD card issues → card too slow, worn out, wrong format, corrupted partition

## Safe First Checks
- Check power supply: must be 5V/3A (Pi 4) or 5V/2.5A (Pi 3) — phone chargers often too weak
- Look for lightning bolt icon in top-right of desktop (undervoltage warning)
- Check SD card is fully seated — card should click in firmly
- Try a different HDMI cable and monitor
- Check USB devices plugged in — high-draw USB devices cause undervoltage
- Boot with nothing connected except power and HDMI

## Tools Needed
- Multimeter (5V supply voltage check)
- Another computer (for SD card re-imaging)
- MicroSD card reader
- Heatsink set (if not installed)

## Step-by-Step Guidance
1. Measure 5V supply at Pi's USB-C (Pi 4) or microUSB (Pi 3) with multimeter — must be 4.9V–5.1V under load. Below 4.75V = replace power supply.
2. Remove all USB peripherals. Retry boot with power+HDMI+SD card only.
3. If rainbow screen → SD card is first suspect. Remove SD card, inspect for physical damage. Try re-imaging with Raspberry Pi Imager on a computer.
4. If new image boots → original card was corrupted. Check card write speed (Class 10 / A1 minimum).
5. If system crashes randomly → check CPU temperature: `vcgencmd measure_temp`. Above 80°C = thermal issue. Install heatsink and/or fan.
6. For GPIO not working → verify pin number in code. Use BCM numbering (GPIO.setmode(GPIO.BCM)) and match pin number to BCM diagram (not physical pin number).
7. For SSH inaccessible → connect monitor/keyboard. Run `hostname -I` to find current IP. Check router DHCP table. Assign static IP in /etc/dhcpcd.conf for stability.
8. For corrupted filesystem → run `sudo fsck /dev/mmcblk0p2` from recovery mode or alternate boot. Back up SD card image once repaired.
9. For persistent undervoltage → check power supply rating, replace cable (cheap cables have high resistance), reduce USB load.
10. If none of above resolve issue → test with known-good SD card and fresh image. If still fails → Pi hardware fault (rare).

## Stop Conditions
- **STOP** if Pi shows burn mark or smell — do not power on again
- **STOP** if GPIO pin is connected to voltage above 3.3V — Pi GPIO is NOT 5V tolerant (permanent damage)
- **STOP** if SD card slot is physically damaged — do not force card in
- Do not operate Pi without adequate power supply — sustained undervoltage degrades SD card

## Prevention
- Use official Raspberry Pi power supply or equivalent with correct amperage
- Add heatsinks before first use — cheap heatsink sets are worthwhile
- Enable automatic SD card check on boot in config
- Use a quality SD card (SanDisk Endurance, Samsung PRO Endurance) — cheap cards fail within months of heavy writes
- Set up automated backups of SD card image monthly

## Keywords
- Raspberry Pi not booting, Pi rainbow screen, Pi undervoltage, Pi no video output
- Pi freezing crashing, Pi overheating throttle, GPIO not working, SD card corrupted
- Pi SSH not working, Pi power supply fault, Raspberry Pi repair, Pi BCM pin numbering
- Pi 4 boot issue, Pi 3 boot issue, lightning bolt warning, Pi SD card read error
