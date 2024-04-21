import argparse
import os
import re
import subprocess
import uuid

import google.generativeai as ggenai
import pandas as pd
from PIL import Image

import ala
import prompts

DS_PATH = "dataset"


def proc_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--adb_path", type=str, default="adb")
    arg_parser.add_argument("--instr", type=str)

    return arg_parser.parse_args()


def get_screenshot(adb_path: str, id: str, iteration: int):
    img_name = f"{id}-{iteration}.png"
    ds_img_path = os.path.join(DS_PATH, "img", img_name)
    cmd = f"{adb_path} shell screencap -p /sdcard/ss.png &&\
            {adb_path} pull /sdcard/ss.png {ds_img_path}"

    subprocess.run(cmd, shell=True)
    print(cmd)

    return Image.open(ds_img_path), "img/" + img_name


def add_resp(item: tuple, role: str, value: str, img_name: str = None):
    c = {"from": role, "value": value}

    if img_name is not None:
        item[1].append(img_name)
    item[2].append(c)


def main():
    cmd_args = proc_args()
    ds_path = os.path.join(DS_PATH, "ala_ds.json")
    ds = pd.read_json(path_or_buf=ds_path, orient="records", lines=True)
    id = str(uuid.uuid4())
    iteration = 0
    item = [id, [], []]
    add_resp(item, "human", "<image>\n" + cmd_args.instr)
    ggenai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = ggenai.GenerativeModel(model_name="gemini-1.5-pro-latest")

    prompt = f"My instruction is: {prompts.instr_ds_prompt} {cmd_args.instr}"
    chat_session = model.start_chat(history=[{
        'role':
        'user',
        'parts': [
            "You are an intelligent and helpful android phone operating assistant. \
            You need to help me operate the phone to perform my instruction."
        ]
    }])

    while True:
        input("Follow Action")
        img, img_name = get_screenshot(cmd_args.adb_path, id, iteration)
        add_resp(item, "human", "<image>", img_name)
        response = chat_session.send_message(
            [prompt, img],
            safety_settings={
                ggenai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
                ggenai.types.HarmBlockThreshold.BLOCK_NONE
            })
        print(response.text)

        action = ""
        try:
            action = re.search(r"Action:(.*)", response.text).group(1).strip()
        except:
            print("retry")

        if "stop" in action:
            break
        else:
            ala.process_action(cmd_args.adb_path, action, img)

        add_resp(item, "gpt", response.text)
        iteration += 1
        prompt = ""

    print(item)
    ds2 = pd.DataFrame((item, ), columns=("id", "image", "conversations"))
    ds = pd.concat((ds, ds2))
    ds_csv_path = os.path.join(DS_PATH, "ala_ds.csv")
    ds.to_json(path_or_buf=ds_path, orient="records", lines=True)
    ds.to_csv(path_or_buf=ds_csv_path, index=False)


if __name__ == "__main__":
    main()
