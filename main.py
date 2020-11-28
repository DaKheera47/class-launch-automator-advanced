import pyautogui as pag
import time
from pick import pick
import yaml
from launcher import main as launcherMain
import schedule


def main():
    # starting time
    t1 = time.time()

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

    # getting standard wait time based on selection
    STANDARD_WAIT = SETUP[SETUP["chosen_speed"]]["duration"]
    pag.PAUSE = round(0.2 * STANDARD_WAIT, 3)

    # mostly for dev
    print(f"pag.PAUSE: {pag.PAUSE}s")
    print(f"Standard wait: {STANDARD_WAIT}s")

    # making choices list with loop
    choices = []

    for class_index in CLASS_INFO:
        current_class = CLASS_INFO[class_index]

        # make choices to display
        choices.append(
            f"Join {class_index} - Code: {current_class['code']}")

    # render picker in cli
    _, selected_index = pick(choices, "Choose Class To Join: ", indicator='=>')

    # select class eg maths
    class_chosen = list(CLASS_INFO)[selected_index]

    # select code and password of that class
    code_to_use = str(CLASS_INFO[class_chosen]["code"])
    password_to_use = str(CLASS_INFO[class_chosen]["password"])

    # calling launcher main
    launcherMain(code_to_use, password_to_use, STANDARD_WAIT, SETUP)

    # printing final execution time
    print(f"Total Execution Time: {round(time.time() - t1, 2)}s")


schedule.every().monday.at("08:00")
