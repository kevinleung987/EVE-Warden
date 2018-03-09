import time
import datetime
from PIL import Image, ImageFilter, ImageGrab
import win32gui
import pytesseract
import json
import difflib
import winsound

with open('config.json') as json_file:
    data = json.load(json_file)
pytesseract.pytesseract.tesseract_cmd = data['tesseract_dir']
tessdata_dir_config = "--tessdata-dir \'"+data['tessdata_dir']+"\'"
window_name = data['window_name']
whitelist = data['whitelist']
w_offset = data['window_offset']
l_offset = data['local_offset']
beep_freq = data['beep_frequency']
diff_cutoff = data['diff_cutoff']
play_sound = data['play_sound']
pixel_detect = data['pixel_detect']
u_replace = data['u_replace']
name_size = data['name_size']
name_offset = data['name_offset']
verbose = data['verbose']
first_neut = True


def get_timestamp():
    """
    Get a formatted timestamp of the current time.
    :return: A String containing the formatted timestamp.
    """
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    return timestamp


def timestamp_print(msg):
    """
    Print the current timestamp to standard output with a message appended.
    :param msg: The message to append.
    :return: None.
    """
    print(get_timestamp()+": "+msg)


def capture_window(offset):
    """
    Captures a screenshot of the window.
    :param offset: The offset to use for capturing the screenshot.
    :return: An Image object representing the screenshot of the window.
    """
    window = win32gui.FindWindow(None, window_name)
    # win32gui.BringWindowToTop(window)
    dimensions = win32gui.GetWindowRect(window)
    dimensions = (dimensions[0] + offset[0], dimensions[1] + offset[1], dimensions[2] + offset[2], dimensions[3] +
                  offset[3])
    img = ImageGrab.grab(bbox=dimensions)
    return img


def upscale(image):
    """
    Pre-processes an image by upscaling and sharpening it to prepare it for text recognition.
    :param image: The image to pre-process.
    :return: The processed, upscaled image.
    """
    image = image.filter(ImageFilter.SHARPEN)
    image = image.resize((image.size[0] * 4, image.size[1] * 4), Image.ADAPTIVE)
    image = image.filter(ImageFilter.SHARPEN)
    return image


def detect_neuts(image):
    """
    Scans the image for a certain colour, indicating the presence of neutrals.
    :param image: The image to scan.
    :return: Set containing all the positions of the neutrals
    """
    neutrals = set()
    imgmap = image.load()
    for i in range (img.size[0]):
        for j in range(img.size[1]):
            r = imgmap[i, j][0]
            g = imgmap[i, j][1]
            b = imgmap[i, j][2]
            if r >= 100:
                if g <= 80:
                    if b <= 30:
                        if len(neutrals) > 0:
                            exists = False
                            for num in neutrals:
                                if (max(num, j)-min(num, j)) <= name_size:
                                    exists = True
                            if not exists:
                                neutrals.add(j)
                        else:
                            neutrals.add(j)
    if len(neutrals) > 0:
        timestamp_print('Pixels with neutrals: '+str(neutrals))
    return neutrals


def read_local(image):
    """
    Returns a list of the current names displayed in the local window
    :param image: An Image of the window
    :return: A list of names displayed in the window
    """
    img = upscale(image)
    local = pytesseract.image_to_string(img, config=tessdata_dir_config).split('\n')
    return local


def read_local_discriminate(image, positions):
    """
    Returns a list of the current names displayed in the local window.
    :param positions: The positions(Top-left pixel) of the names to look for.
    :param image: An Image of the window.
    :return: A list of names displayed in the window.
    """
    local = []
    for pos in positions:
        temp_img = image.crop((0, pos-name_offset, image.size[0], pos+name_size+name_offset))
        temp_img = upscale(temp_img)
        temp_img.save('neutral.png')
        local.append(pytesseract.image_to_string(temp_img, config=tessdata_dir_config))
    return local


def detect_local(local):
    """
    Checks the list of neutrals against the white-list, if there are non-whitelisted neutrals then they are appended
    to a list to be returned. If a name is within a cutoff of similarity to a whitelisted name, it will count as being
    whitelisted.
    :param local: The list of neutrals to check against the white-list.
    :return: A list of neutrals that are not on the white-list.
    """
    not_whitelisted = []
    for name in local:
        if len(name) <= 3:
            pass
        else:
            matches = difflib.get_close_matches(name, whitelist, 1, diff_cutoff)
            if len(matches) == 0:
                if u_replace:
                    temp = name.replace('u', 'y')
                    matches = difflib.get_close_matches(temp, whitelist, 1, diff_cutoff)
                    if len(matches) == 0:
                        not_whitelisted.append(name)
                else:
                    not_whitelisted.append(name)
    return not_whitelisted


if __name__ == '__main__':
    while True:
        neutrals = set()
        img = capture_window(w_offset)
        if pixel_detect: # If only scanning for neutrals when red/orange pixels present.
            neutrals = detect_neuts(img)
            neutral_present = len(neutrals) > 0
        else:
            neutral_present = True
        if neutral_present:
            img = capture_window(l_offset)
            if pixel_detect:
                # If looking for red/orange pixels, only scan those names with red/orange pixels next to them.
                local = read_local_discriminate(img, neutrals)
            else:
                local = read_local(img)
            timestamp_print("Neutrals: "+str(local))
            hostiles = detect_local(local)
            if len(hostiles) > 0:
                timestamp_print("Non-whitelisted Neutrals: "+str(hostiles))
                if play_sound:
                    winsound.PlaySound("alert.wav", 8256)
                else:
                    winsound.Beep(beep_freq, 1000)
                time.sleep(30)
            else:
                timestamp_print("Neutrals detected, but all whitelisted")
        else:
            if verbose:
                timestamp_print("No Neutrals detected")
        time.sleep(2)
