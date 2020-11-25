import pyautogui as pag
import time
import yaml
from launcher import main as launcherMain
import schedule
import datetime

# importing external files
with open("config.yaml", 'r') as stream:
    try:
        SETUP = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open("classes.yaml", 'r') as stream:
    try:
        CLASS_INFO = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def getCodeAndPass(cls):
    # select code and password of that class
    code_to_use = str(CLASS_INFO[cls]["code"])
    password_to_use = str(CLASS_INFO[cls]["password"])
    return (code_to_use, password_to_use)


def main():
    currTime = datetime.datetime.now().strftime("%H:%M")
    currDay = datetime.datetime.today().weekday()
    print(f"called main: {currTime}")

    # getting standard wait time based on selection
    STANDARD_WAIT = SETUP[SETUP["chosen_speed"]]["duration"]
    pag.PAUSE = round(0.2 * STANDARD_WAIT, 3)

    for cls in CLASS_INFO.items():
        if currTime == cls[1]["time_weekday"] and currDay in range(3):
            code_to_use, password_to_use = getCodeAndPass(cls[0])
            print(
                f"Using {cls[0]} class information \n Code: {code_to_use} \n Pass: {password_to_use}")
            launcherMain(code_to_use, password_to_use, STANDARD_WAIT, SETUP)
            print(
                f"Successfully launched {cls[0]} class and now waiting for next class time!")

        elif currTime == cls[1]["time_friday"] and currDay == 4:
            # if cls[0] == "Chemistry":
            code_to_use, password_to_use = getCodeAndPass(cls[0])
            print(
                f"Using {cls[0]} class information \n Code: {code_to_use} \n Pass: {password_to_use}")
            launcherMain(code_to_use, password_to_use, STANDARD_WAIT, SETUP)
            print(
                f"Successfully launched {cls[0]} class and now waiting for next class time!")


schedule.every(30).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
