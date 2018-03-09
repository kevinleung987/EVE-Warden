# EVE-Warden
A tool for EVE Online which detects hostile neutrals in the present system by reading and analyzing the Local Window.

![](example.png?raw=true)

The image above shows an example usage of this tool.
On the Left is the console output. 
On the Right is the cropped section of the EVE window that is being monitored. 
In the Middle is the name of the neutral(Indicated by the blinking red symbol) that has been cropped out to be processed by Tesseract.

## Getting Started
- This program is meant to be used in conjunction with a screen cropping tool like OnTopReplica, but by simply keeping the EVE Online window in focus and with the right offset values, you can run it with just EVE as well.
- Clone the repository and get the dependencies setup, you will need to install Google Tesseract as well if you want to use the text recognition features. Tesseract 3 is currently being used for this project, but 4 may work as well.
- Downloading and running the compiled executable found in the Releases page works as well.
- Modify config.json with your desired values, you can also run the calibrator which will display what the offsets look like. Other flags in the config file like the path to Tesseract or the process name may also require modification

## Flags
- `tesseract_dir` The path to your Tesseract executable.
- `tessdata_dir` The path to the tessdata directory.
- `window_name` The name of the process to monitor.
- `whitelist` A list of white-listed names that will not trigger the alarm. If a name is found that is similar to a white-listed name, it will also not trigger the alarm.
- `diff_cutoff` How different a name has to be from the white-listed names in order to trigger the alert.
- `beep_frequency` The frequency that the alarm will have. This value only gets used if `play_sound` is `false`.
- `play_sound` If `true`, will play the sound `alert.wav`, otherwise it will emit a beep with the frequency of `beep_frequency`.
- `pixel_detect` If `true`, will cause the text recognition to only trigger when red/orange pixels are detected in the window, indicating a neutral. Otherwise, it will consider there to always be neutrals and check against white-listed names.
- `u_replace` The font in EVE Online has "y" and "u" being too similar for Tesseract to discriminate against, enable this if that is causing issues.
- `window_offset` Tuple of (Top-Left, Top-Right, Bottom-Left, Bottom-Right) values to be used as offsets for the Window dimensions. These offsets should be large enough to capture the entirety of the names+standings of the Local window.
- `local_offset` Values to be used as offsets for the Window dimensions when capturing just the names, these offsets should capture just the names in the Local window.
- `name_size` The number of pixels that the height of a name in the Local window is. (This will be automated in the future)
- `name_offset` A small offset so the names do not get cut off, should be around 1/5 or 1/6 the value of `name_size`
- `verbose` Whether the logs of the program should be verbose or not.

## Dependencies

* [Pillow](https://github.com/python-pillow/Pillow) - Used to manipulate images and grab screen data.
* [pytesseract](https://github.com/madmaze/pytesseract) - OCR framework for recognizing names.
* [win32gui](https://pypi.python.org/pypi/win32gui/221.6) - Used to grab window dimensions and locations or to bring windows to focus.

License
----
MIT