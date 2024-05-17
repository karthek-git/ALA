import argparse
import os
import re
import subprocess
import time

import google.generativeai as ggenai
import PIL
import pytesseract

import actuator
import prompts


def proc_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--adb_path", type=str)
    arg_parser.add_argument("--g_api_key",
                            default=os.getenv("GOOGLE_API_KEY"),
                            type=str)

    return arg_parser.parse_args()


def get_text_coordinates(txt: str, img):
    r = pytesseract.image_to_data(img).splitlines()
    boxes = [x.split()[6:] for x in r]

    for box in boxes:
        if txt in box[-1]:
            return box[:2]


def process_action(adb_path: str, action: str, img):
    if "click text" in action:
        param = re.search(r"\((.*?)\)", action).group(1)
        x, y = get_text_coordinates(param, img)
        cmd = f"{adb_path} shell input tap {x} {y}"
        print(f"Tap at ({x},{y})")
        subprocess.run(cmd, shell=True)
    elif "click icon" in action:
        pass
    elif "page" in action:
        x, y = actuator.get_size(adb_path)
        actuator.slide(adb_path, action, x, y)
    elif "type" in action:
        txt = re.search(r"\((.*?)\)", action).group(1)
        actuator.type(adb_path, txt)
    elif "wait" in action:
        duration = re.search(r"\((.*?)\)", action).group(1)
        time.sleep(duration)
    elif "back" in action:
        actuator.back(adb_path)
    elif "exit" in action:
        actuator.back_to_desktop(adb_path)
    else:
        print("error in prforming action")


def main():
    cmd_args = proc_args()
    adb_path = cmd_args.adb_path

    ggenai.configure(api_key=cmd_args.g_api_key)
    model = ggenai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    chat_session = model.start_chat(history=[])

    print("You:", end=" ")
    usr_instr = input()

    while True:
        input("Follow Action")
        cmd = f"{adb_path} shell screencap -p /sdcard/ss.png && {adb_path} pull /sdcard/ss.png"
        subprocess.run(cmd, shell=True)

        img = PIL.Image.open("ss.png")
        prompt = prompts.instr_prompt + usr_instr
        print(prompt)
        response = chat_session.send_message(
            [prompt, img],
            safety_settings={
                ggenai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
                ggenai.types.HarmBlockThreshold.BLOCK_NONE
            })
        print(f"Ala:{response.text}")

        try:
            action = re.search(r"Action:(.*)", response.text).group(1).strip()
        except:
            print("retry")

        if "stop" in action:
            break
        else:
            process_action(action)

        process_action(adb_path, action)


if __name__ == "__main__":
    main()
