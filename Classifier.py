import shutil
import os
import time
import json

CONFIG_FILE = "classifier"

FILE_EXTENSION = {"Media": ("avi", "mkv", "mp4", "mp3", "pdf",
                            "txt", "epub", "doc", "csv", "xml", "wav", "jpg", "wma", "bmp"), "Other": ("exe", "zip", "7z", "iso"), }
TIME = "TIME"
FLAG_FILE = "FLAG_FILE"
ONLY_ONCE = "ONLY_ONCE"


def ReadConfigFile():
    with open(CONFIG_FILE, "r") as file:
        return json.loads(file.read())


def createCofigFile():
    with open(CONFIG_FILE, "w") as file:
        file.write(json.dumps(
            {"FILE_EXTENSION": FILE_EXTENSION, "TIME": 1, "FLAG_FILE": True, "ONLY_ONCE": False}))


def main():
    if not os.path.exists(CONFIG_FILE):
        createCofigFile()
    configFile = ReadConfigFile()
    flag = configFile[FLAG_FILE]

    for directory in configFile["FILE_EXTENSION"]:
        if not os.path.exists(directory):
            os.makedirs(directory)

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
        for file in os.listdir():
            if "." in file:
                f = file.split(".")
                f, extension = "".join(f[:-1]), f[-1]
                for directory in configFile["FILE_EXTENSION"]:
                    if extension in configFile["FILE_EXTENSION"][directory]:
                        shutil.move(file,
                                    os.path.join(os.getcwd(), directory))
        if configFile[ONLY_ONCE]:
            break
        time.sleep(configFile[TIME])


if __name__ == '__main__':
    main()
