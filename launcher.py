import pyautogui as pag
import time
import os
import sys


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def findImage(imageUrl, message, confidence):
    i = 1

    while True:
        time.sleep(1)
        try:
            joinMeetingX, joinMeetingY = pag.locateCenterOnScreen(
                imageUrl, confidence=confidence)
        except TypeError:
            print(f"{message} (attempts: {i})", end="\r")
            i += 1
            continue
        break

    clear()
    return (joinMeetingX, joinMeetingY)


def checkAbsence(imageUrl, message):
    i = 1

    while True:
        location = pag.locateOnScreen(imageUrl)

        if location == None:
            break
        else:
            print(
                f"{message} (attempts: {i})", end="\r")

        time.sleep(5)
        i += 1

    clear()


def enterTextInput(x, y, text, message):
    pag.click(x=x, y=y)
    pag.write(text)
    print(f"\n{message}")
    pag.press("enter")


def main(code, password, STANDARD_WAIT, SETUP):
    if SETUP["launch_method"] == "executable":
        # extracting executable location from config.yaml
        zoomExe = SETUP['zoom_executable_location']

        if zoomExe != None and os.path.exists(zoomExe):
            # if zoom path isnt empty and it is valid
            cwd = os.getcwd()
            os.chdir(r"C:\Users\dakonwindows\AppData\Roaming\Zoom\bin")
            os.system(f"start "" Zoom.exe")
        else:
            # if the file path provided is incorrect
            sys.exit(
                "ERROR: launch_method chosen is executable but no executable path is provided or the path provided is incorrect")

    elif SETUP["launch_method"] == "startMenu":
        # start button
        pag.press("win")

        # launch zoom
        pag.write("Zoom")
        pag.press("enter")
    else:
        sys.exit("ERROR: launch_method is unsupported in config.yaml")

    # resetting cwd back to original to use images in that folder
    os.chdir(cwd)

    # wait for zoom to launch
    time.sleep(10)

    # locate join button on zoom
    joinX, joinY = findImage(
        "joinBtn.png", "Join button not found... Searching again", 0.8)
    pag.click(x=joinX, y=joinY)

    # enter code into meeting id field
    joinMeetingX, joinMeetingY = findImage(
        "joinMeeting.png", "Join Meeting button not found... Searching again", 0.8)
    enterTextInput(joinMeetingX, joinMeetingY + 60, code, "Code entered!")

    # enter password into password field
    enterPassX, enterPassY = findImage(
        "enterMeetingPw.png", "Enter Meeting Password text not found... Searching again", 0.8)
    enterTextInput(enterPassX, enterPassY + 60, password, "Password entered!")

    # wait for password to be accepted
    time.sleep(10)

    # locate join with computer audio button on zoom
    pag.click(findImage("joinWithComputerAudioBtn.PNG",
                        "Have not joined class yet... Searching again", 0.8))

    # force full screen zoom
    pag.hotkey("win", "up")
