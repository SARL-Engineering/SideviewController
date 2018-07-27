# ![](https://github.com/SARL-Engineering/SideviewController/blob/master/icon.PNG) Sideview Controller

## About
Custom software for performing Sideview Unit experiments.  Only for Windows 10.  Currently, a single FLIR camera views 8 tanks adjacent to two monitors with timed triggers for LEDs and tank tapping.  Sideview Controller was written with modularity in mind, so any number of cameras, monitors, or COM devices may be set up.

## Usage
![](https://github.com/SARL-Engineering/SideviewController/blob/master/sv_screenshot.PNG)
1. Use the Browse button to select an output folder for the recorded video(es).
2. Right below that button, select whether the recording time will be based on an exact time, or just based on the length of the video that will be used.
3. Using the Cameras, Screens, and COMs tabs, use the Add button to add links to the respective devices you'd like to use for a recording.  Screens contain options for both videoes and single colors.  Note that the "Specified time" option must be used if you're only going to use flat colors.
4. Use the Open button on each of the devices added to bring up windows for their usage.  **Devices that are not opened in windows will not be used in recording.**
5. Press the big play button!

### COM Devices
Adding devices for timed signal-based interactions is slightly more involved.  In addition to setting the parameters listed in the dialog box, you will need to add one or more **Rules**.  Rules are the trigger points for sending signals to an attached serial device.  

![](https://github.com/SARL-Engineering/SideviewController/blob/master/sv_screenshot2.PNG)

There are two types of Rules, **Signal At** and **Signal Every**.  Signal At simply means that the trigger will occur at the selected time.  Signal Every means that the trigger will occur repeatedly with a delay.  The selected time will be this delay.  

![](https://github.com/SARL-Engineering/SideviewController/blob/master/sv_screenshot3.PNG)

You can make more complex Rules using the Interval feature.  If you check Interval, then the trigger will be restricted to the time interval that you indicate.  For example, a Signal Every of 5 seconds with an Interval of 10 and 30 seconds means that the trigger will not start until 10 seconds, then trigger every 5 seconds until 30 seconds in total have elapsed (20 seconds of triggering).

### Saving Configs
You can save your setup to a config file so you can quickly load and record between uses of the software.  Basically you can create a config for each experiment to ensure the parameters stay consistent for each different test.  It's all in the File menu.

## Development - Deployment
Compiled using `pyinstaller` with the options located in `pyinstaller_build.txt`  Then [Inno Setup](http://www.jrsoftware.org/isinfo.php) is used to generate an installer.  Codecs are *probably* going to be an issue so I recommend bundling the [K-Lite Codec Pack (Basic)](https://codecguide.com/download_kl.htm) with this installer for proper deployment.  The exact script I used for this is in `installer_script.iss`

## Development - Notable Dependencies
* ffmpeg - Necessary for proper video playback on experiment monitors
* opencv_ffmpeg341_64.dll
* PySpin - Custom wrapper of FLIR firmware
* SpinView/Spinnaker SDK - Many dlls needed for FLIR camera to even appear as a camera device