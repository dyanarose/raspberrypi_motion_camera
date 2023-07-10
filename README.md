# RaspberryPi Motion Activated Camera

Compatible with 
- Raspberry Pi OS Lite Debian 11 (bullseye)
- Raspberry Pi Camera Module 3
- PIR Motion Sensor

## TOML Configuration
```toml
[storage]
path="/media/usb/" # save images to this folder
datetime_format="%Y-%d-%mT%H_%M_%S" # datetime format for the image file name
```

## Requirements
- [picamera2](https://www.raspberrypi.com/news/picamera2-beta-release/) should already be installed.
- `pip install tomli gpiozero`

If you need to install pip, you can find instructions on [pip's documentation site](https://pip.pypa.io/en/stable/installation/).


## Gotchas (or Got Me's)
### Motion Sensor Settings
PIR Motion Sensors have a few physical settings. Take this common [PIR sensor](https://thepihut.com/products/pir-motion-sensor-module).

It has three settings on the board.
- A screw to change the maximum distance of the sensor. Left to reduce, right to increase
- A screw to change the delay when changing from High to Low voltage. Left to reduce, right to increase.
- A jumper that alternates between L and H. 
To change the jumper, pull it off the two pins it's on, and move it to the other two pins. 
If the jumper is covering L, it's in L mode, if it's covering H, it's in H mode.
  - Set it to H for this code. That keeps the voltage at High until the delay period ends, then it drops to Low.
  - An L setting will alternate between High and Low while activity is detected and then stay at low when the delay period ends.

![image](https://content.instructables.com/F3I/YKYD/JU31W6C1/F3IYKYDJU31W6C1.jpg)

### Permissions issues when saving images
You will need to grant Write permissions on the image directory to the user running the code.

If you are using a mounted drive, and it's formatted as `FAT32` or `NTFS` you will not be able to change permissions via `chown, chmod, etc.`
This [Ask Ubuntu answer has settings you can try](https://askubuntu.com/questions/96923/how-do-i-change-permissions-on-a-fat32-formatted-drive) but IMO reformatting the drive as `ext4` is a lot faster.


## Waterproof cases
- [Natuebytes Wildlife Camera case](https://thepihut.com/products/naturebytes-wildlife-camera-case)
  - I advise only buying the case (not the kit) and using your own electronics unless you are desperate for a Raspberry Pi A+.