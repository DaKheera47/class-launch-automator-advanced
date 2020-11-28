import pyautogui as pag
import time
import os
import sys


def main(code, password, STANDARD_WAIT, SETUP):
    if SETUP["launch_method"] == "executable":
        # extracting executable location from config.yaml
        zoomExe = SETUP['zoom_executable_location']

        if zoomExe != None and os.path.exists(zoomExe):
            # if zoom path isnt empty and it is valid
            print("path exists")
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

    print(cwd)
    os.chdir(cwd)

    # wait for zoom to launch
    time.sleep(10)

    print("Zoom should be launched!")

    # locate join button on zoom
    join = pag.locateCenterOnScreen("joinBtn.PNG")

    while join == None:
        print("button not found")
        join = pag.locateCenterOnScreen("joinBtn.PNG")

    print("Join Button Found! Clicking join")
    pag.click(join)

    # enter code into meeting id field
    time.sleep(STANDARD_WAIT)
    pag.write(code)
    print("Code Entered!")
    pag.press("enter")

    # enter password into meeting id field
    time.sleep(STANDARD_WAIT + 2)
    pag.write(password)
    print("Password Entered!")
    pag.press("enter")

    # wait for password to be accepted
    time.sleep(10)

    hasMeetingStarted = False

    for _ in range(180):
        time.sleep(5)

        while hasMeetingStarted == False:
            meeting = pag.locateOnScreen('pleaseWaitForMeeting.png')
            if meeting == None:
                hasMeetingStarted = True
            else:
                print("Meeting hasn't started yet")

        a = pag.locateOnScreen('testComputerAudioBtn.png')
        if a == None:
            print("Host accepted")
            break
        else:
            print("Host has not accepted yet")

    # locate join with computer audio button on zoom
    time.sleep(STANDARD_WAIT)
    pag.click(pag.locateCenterOnScreen("joinWithComputerAudioBtn.PNG"))

    # force full screen zoom
    pag.hotkey("win", "up")
