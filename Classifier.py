import shutil
import os
import time
import json
import datetime

CONFIG_FILE = "classifier"

FILE_EXTENSION = {"Media": (os.path.join(os.getcwd(), "Media"), ("avi", "mkv", "mp4", "mp3", "pdf",
                                                                 "txt", "epub", "doc", "csv", "xml", "wav", "jpg", "wma", "bmp")),
                  "Other": (os.path.join(os.getcwd(), "Other"), ("exe", "zip", "7z", "iso"))}
SCAN_TIME = "SCAN_TIME"
FLAG_FILE = "FLAG_FILE"
ONLY_ONCE = "ONLY_ONCE"
FILE_TIME = "FILE_TIME"
TYPE_TIME = "TYPE_TIME"


def ReadConfigFile():
    with open(CONFIG_FILE, "r") as file:
        return json.loads(file.read())


def createCofigFile():
    with open(CONFIG_FILE, "w") as file:
        file.write(json.dumps(
            {"FILE_EXTENSION": FILE_EXTENSION, SCAN_TIME: 1, FLAG_FILE: True, ONLY_ONCE: False, FILE_TIME: 10, TYPE_TIME: 60}))


def main():
    if not os.path.exists(CONFIG_FILE):
        createCofigFile()
    configFile = ReadConfigFile()
    flag = configFile[FLAG_FILE]

    for directory in configFile["FILE_EXTENSION"]:
        if not os.path.exists(configFile["FILE_EXTENSION"][directory][0]):
            os.makedirs(configFile["FILE_EXTENSION"][directory][0])

    cash = {}
    if flag:
        if not os.path.exists(FLAG_FILE):
            with open(FLAG_FILE, "w") as file:
                pass
    else:
        if os.path.exists(FLAG_FILE):
            os.remove(FLAG_FILE)

    while True:
        if flag:
            if not os.path.exists(FLAG_FILE):
                break
        time_now = datetime.datetime.now().replace(microsecond=0)
        for file in os.listdir():
            if file in cash:
                if (datetime.datetime.now() - cash[file]).seconds > configFile[FILE_TIME] * configFile[TYPE_TIME]:
                    if "." in file:
                        f = file.split(".")
                        f, extension = "".join(f[:-1]), f[-1]
                        for directory in configFile["FILE_EXTENSION"]:
                            if extension in configFile["FILE_EXTENSION"][directory][1]:
                                shutil.move(
                                    file, configFile["FILE_EXTENSION"][directory][0])

            else:
                cash[file] = datetime.datetime.now()

        if configFile[ONLY_ONCE]:
            break
        time.sleep(configFile[SCAN_TIME] * configFile[TYPE_TIME])


if __name__ == '__main__':
    main()
