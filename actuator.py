import time
import subprocess
from PIL import Image


def get_size(adb_path):
    command = adb_path + " shell wm size"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    resolution_line = result.stdout.strip().split('\n')[-1]
    width, height = map(int, resolution_line.split(' ')[-1].split('x'))
    return width, height


def tap(adb_path, x, y, px, py):
    w = px
    h = py
    ax = int(x*w)
    ay = int(y*h)
    command = adb_path + f" shell input tap {ax} {ay}"
    subprocess.run(command, capture_output=True, text=True, shell=True)
    time.sleep(1)


def type(adb_path, text):
    text = text.replace("\\n", "_").replace("\n", "_")
    for char in text:
        if char == ' ':
            command = adb_path + f" shell input text %s"
            subprocess.run(command, capture_output=True, text=True, shell=True)
        elif char == '_':
            command = adb_path + f" shell input keyevent 66"
            subprocess.run(command, capture_output=True, text=True, shell=True)
        elif 'a' <= char <= 'z' or 'A' <= char <= 'Z' or char.isdigit():
            command = adb_path + f" shell input text {char}"
            subprocess.run(command, capture_output=True, text=True, shell=True)
        elif char in '-.,!?@\'°/:;()':
            command = adb_path + f" shell input text \"{char}\""
            subprocess.run(command, capture_output=True, text=True, shell=True)
        else:
            command = adb_path + f" shell am broadcast -a ADB_INPUT_TEXT --es msg \"{char}\""
            subprocess.run(command, capture_output=True, text=True, shell=True)
    time.sleep(1)


def slide(adb_path, action, x, y):
    if "down" in action:
        command = adb_path + f" shell input swipe {int(x/2)} {int(y/2)} {int(x/2)} {int(y/4)} 500"
        subprocess.run(command, capture_output=True, text=True, shell=True)
    elif "up" in action:
        command = adb_path + f" shell input swipe {int(x/2)} {int(y/2)} {int(x/2)} {int(3*y/4)} 500"
        subprocess.run(command, capture_output=True, text=True, shell=True)
    time.sleep(1)


def back(adb_path):
    command = adb_path + f" shell input keyevent 4"
    subprocess.run(command, capture_output=True, text=True, shell=True)
    time.sleep(1)
    
    
def back_to_desktop(adb_path):
    command = adb_path + f" shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
    subprocess.run(command, capture_output=True, text=True, shell=True)
    time.sleep(1)
