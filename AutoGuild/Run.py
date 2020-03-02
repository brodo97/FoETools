try:
    import time
    import cv2
    import mss
    import numpy as np
    import pyautogui as p
    import os
    import requests
    import urllib
    import yaml
    import sys
    from datetime import datetime
except Exception as e:
    input("Missing lib: {}. [Enter] to quit.".format(e))
    exit()


class ReadImage:
    def __init__(self, name):
        self.data = cv2.imread(name)
        self.__name = name

    def __str__(self):
        return self.__name


def sleep(waitTime):
    print("\nTime passed: {:.2f}s\nAssist: {}".format(time.time() - ts, assistCount))
    time.sleep(waitTime)


def search(image, t):
    print("Looking for: {}".format(image))
    template = image.data
    capture = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_RGBA2RGB)
    res = cv2.matchTemplate(capture, template, cv2.TM_CCOEFF_NORMED)
    return (len(template[0]), len(template), list(zip(*np.where(res >= t)[::-1])))


if __name__ == '__main__':

    FILE_NAME = sys.argv[0]
    TOTAL = [0, 0, 0, 0, 0]
    SESSIONS = []
    VERSION = 0.8
    SETTINGS = {}
    DEFAULT = {"version": VERSION, "enter": "EnterGuild.PNG", "guildTab": "GuildTab.PNG", "friendsTab": "FriendsTab.PNG", "neighborsTab": "NeighborsTab.PNG", "globalBtn": "Global.PNG", "globalGuild": "GlobalGuild.PNG", "members": "Members.PNG", "quit": "QuitGuild.PNG", "down": "Down.PNG", "leave": "LeaveGuild.PNG", "button0": "First.PNG", "button1": "Next.PNG", "assist": "Assist.PNG", "tavern": "Tavern.PNG", "exit": "Exit.PNG", "threshold": 0.91, "phase": -1, "waitAction": 1, "waitAssist": 1.5, "waitReload": 10, "maxTimeNoAssists": 60, "telegramID": "", "telegramToken": ""}
    PARAMS = ["#Settings", "#Buttons", "enter", "guildTab", "friendsTab", "neighborsTab", "globalBtn", "globalGuild", "members", "quit", "down", "leave", "button0", "button1", "assist", "tavern", "exit", "#Template matching threshold", "threshold", "#Starting phase", "phase", "#Wait times in seconds", "waitAction", "waitAssist", "waitReload", "maxTimeNoAssists", "#Telegram", "telegramID", "telegramToken"]

    if input("1) Log into your FoE's account\n2) Keep the window visible\n3) Run it\nIf you want to stop the script, just move the cursor in the top left corner of your monitor.\nUnderstand? (y/N): ").lower() != "y":
        exit()

    if "Settings.yml" in os.listdir("."):
        with open("Settings.yml") as _F:
            try:
                SETTINGS = yaml.load(_F, Loader=yaml.FullLoader)
            except Exception:
                try:
                    SETTINGS = yaml.load(_F)
                except Exception:
                    input("Can't read Settings.yml. [Enter] to quit.")
                    exit()

    # Settings.yml fixer and updater
    if "version" not in SETTINGS or float(SETTINGS["version"]) < VERSION or len(DEFAULT) != len(SETTINGS):
        with open("Settings.yml", "w") as _F:
            _F.write("version: {}\n".format(VERSION))
            for param in PARAMS:
                if "#" in param:
                    _F.write("{}\n".format(param))
                else:
                    if param in SETTINGS and SETTINGS[param] != DEFAULT[param]:
                        _F.write("{}: {}\n".format(param, SETTINGS[param]))
                    else:
                        _F.write("{}: {}\n".format(param, DEFAULT[param]))
                        SETTINGS[param] = DEFAULT[param]

    # CSV History
    if "Data.csv" in os.listdir("."):
        getTotal, getSessions = 0, 0
        with open("Data.csv") as _F:
            for line in _F:
                if "#Time" in line:
                    getTotal = 1
                    continue
                if "#From" in line:
                    getSessions = 1
                    continue

                if getTotal:
                    getTotal = 0
                    TOTAL = list(map(int, line.rstrip().split(",")))
                if getSessions:
                    SESSIONS.append(line.rstrip())

    enter = ReadImage(SETTINGS["enter"])
    guildTab = ReadImage(SETTINGS["guildTab"])
    friendsTab = ReadImage(SETTINGS["friendsTab"])
    neighborsTab = ReadImage(SETTINGS["neighborsTab"])
    globalBtn = ReadImage(SETTINGS["globalBtn"])
    globalGuild = ReadImage(SETTINGS["globalGuild"])
    members = ReadImage(SETTINGS["members"])
    quit = ReadImage(SETTINGS["quit"])
    down = ReadImage(SETTINGS["down"])
    leave = ReadImage(SETTINGS["leave"])
    buttons = {0: ReadImage(SETTINGS["button0"]), 1: ReadImage(SETTINGS["button1"])}
    assist = ReadImage(SETTINGS["assist"])
    tavern = ReadImage(SETTINGS["tavern"])
    exit = ReadImage(SETTINGS["exit"])

    threshold = SETTINGS["threshold"]
    phase = SETTINGS["phase"]

    waitAction = SETTINGS["waitAction"]
    waitAssist = SETTINGS["waitAssist"]
    waitReload = SETTINGS["waitReload"]
    maxTimeNoAssists = SETTINGS["maxTimeNoAssists"]

    telegramID = SETTINGS["telegramID"]
    telegramToken = SETTINGS["telegramToken"]

    missingCount = 0
    assistCount = 0
    projectsCount = 0
    guildCount = 0
    errorCount = 0
    reloadCount = 0
    ts = time.time()
    lastAssist = time.time()
    phasesList = []

    try:
        with mss.mss() as sct:
            monitor = sct.monitors[0]

            if input("Enable 'Full Auto FoE SitAss Mode'? (Assist neighbors, friends and sit in taverns) (y/N): ").lower() == "y":
                tabs = {0: ReadImage(SETTINGS["friendsTab"]), 1: ReadImage(SETTINGS["neighborsTab"])}
                tab = 0

                while tab in tabs:
                    w, h, point = search(tabs[tab], threshold)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        sleep(waitAction)
                        button = 0

                        while "Looking for buttons":
                            if missingCount > 3:
                                missingCount = 0
                                break

                            w, h, point = search(buttons[button], threshold)

                            if point:
                                if button == 0:
                                    button = 1

                                p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                                p.click()
                                sleep(waitAssist)

                                while "Looking for assists":
                                    w, h, points = search(assist, threshold)

                                    if points:
                                        missingCount = 0
                                        for point in points:
                                            p.moveTo(point[0] + w // 2, point[1] + h // 2)
                                            p.click()
                                            assistCount += 1
                                            sleep(waitAction)
                                    else:
                                        print("{} not found".format(assist))
                                        missingCount += 1
                                        break

                                while "Looking for taverns":
                                    w, h, points = search(tavern, threshold)

                                    if points:
                                        missingCount = 0
                                        for point in points:
                                            p.moveTo(point[0] + w // 2, point[1] + h // 2)
                                            p.click()
                                            sleep(waitAction)
                                    else:
                                        print("{} not found".format(tavern))
                                        missingCount += 1
                                        break
                            else:
                                print("Error: {} not found".format(buttons[button]))
                                break
                    else:
                        print("{} not found".format(tabs[tab]))

                    tab += 1

            lastAssist = time.time()

            while "Automate":
                phasesList.append(phase)

                if time.time() - lastAssist > maxTimeNoAssists:
                    print("No assist in the last {} seconds. Reloading".format(maxTimeNoAssists))
                    p.press("f5")
                    reloadCount += 1
                    phasesList.append("Reload")

                    if telegramToken and telegramID:
                        try:
                            message = "Bot stuck somewhere, reloading.\nLast {} phases: *{}*".format(100 if len(phasesList) > 100 else len(phasesList), phasesList[-100:])
                            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(telegramToken, telegramID, urllib.parse.quote_plus(message)))
                        except Exception as e:
                            print(e)

                    sleep(waitReload)
                    lastAssist = time.time()
                    phase = -1

                if phase == -1:
                    w, h, point = search(guildTab, threshold)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        sleep(waitAction)
                        phase = 0

                        w, h, point = search(buttons[0], threshold)

                        if point:
                            p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                            p.click()
                            sleep(waitAction)
                        else:
                            print("{} not found. What's happening?".format(buttons[0]))

                    else:
                        print("{} not found".format(guildTab))
                        w, h, point = search(exit, threshold)

                        if point:
                            p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                            p.click()
                            sleep(waitAction)
                            phase = 0
                        else:
                            print("{} not found".format(exit))

                            p.press("esc")
                            sleep(waitAction)
                            p.press("esc")

                # ENTER GUILD BUTTON
                elif phase == 0:
                    w, h, point = search(enter, threshold)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        sleep(waitAction)
                        p.press("esc")
                        sleep(waitAction)
                        p.press("esc")
                        sleep(waitAction)
                        guildCount += 1
                        missingCount = 0
                        phase = 2
                    else:
                        w, h, points = search(assist, threshold)

                        if points:
                            phase = 2
                        else:
                            phase = 1

                # NEXT GUILDS PAGE BUTTON
                elif phase == 1:
                    w, h, point = search(buttons[1], threshold)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        sleep(waitAction)
                        missingCount += 1
                        phase = 0
                        print("{} not found: {}".format(enter, missingCount))

                        if missingCount > 3:
                            missingCount = 0
                            phase = 3
                    else:
                        print("Error: {} not found".format(buttons[1]))
                        break

                # ASSIST
                elif phase == 2:
                    button = 0

                    while "Looking for buttons":
                        if missingCount > 1:
                            missingCount = 0
                            phase = 3
                            break

                        w, h, point = search(buttons[button], threshold)

                        if point:
                            if button == 0:
                                button = 1

                            p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                            p.click()
                            sleep(waitAssist)
                            cycle = 0

                            while "Looking for assists":
                                w, h, points = search(assist, threshold)

                                if points:
                                    if missingCount == 0 and cycle:
                                        projectsCount += 1
                                    missingCount = 0
                                    for point in points:
                                        p.moveTo(point[0] + w // 2, point[1] + h // 2)
                                        p.click()
                                        assistCount += 1
                                        lastAssist = time.time()
                                        sleep(waitAction)
                                        cycle = 1
                                else:
                                    cycle = 0
                                    missingCount += 1
                                    print("{} not found: {}".format(assist, missingCount))
                                    break
                        else:
                            print("Error: {} not found".format(buttons[button]))

                # GLOBAL BUTTON
                elif phase == 3:
                    w, h, point = search(enter, threshold)

                    if point:
                        phase = 0
                        continue

                    w, h, point = search(globalBtn, threshold)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        p.moveRel(100)
                        sleep(waitAction)
                        phase = 4
                    else:
                        p.press("esc")
                        sleep(waitAction)
                        errorCount += 1
                        print("{} not found: {}".format(globalBtn, errorCount))
                        if errorCount > 3:
                            errorCount = 0
                            print("Error: {} not found. Where am I? Quit".format(globalBtn))
                            break

                # GLOBAL -> GUILD BUTTON
                elif phase == 4:
                    w, h, point = search(globalGuild, 0.98)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        sleep(waitAction)
                        phase = 5
                    else:
                        sleep(waitAction)
                        missingCount += 1
                        print("{} not found: {}".format(globalGuild, missingCount))
                        if missingCount > 3:
                            missingCount = 0
                            print("{} not found. Where am I?".format(globalGuild))
                            phase = 3

                # GUILD MEMBERS BUTTON
                elif phase == 5:
                    w, h, point = search(members, threshold)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        sleep(waitAction * 2)
                        phase = 6
                    else:
                        print("{} not found".format(members))

                # QUIT GUILD BUTTON
                elif phase == 6:
                    while "Searching":
                        w, h, point = search(quit, 0.99)

                        if point:
                            p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                            p.click()
                            sleep(waitAction)
                            phase = 7
                            break
                        else:
                            missingCount += 1
                            print("{} not found: {}".format(quit, missingCount))
                            if missingCount > 12:
                                missingCount = 0
                                print("Error: {} not found. Where am I?".format(quit))
                                phase = 3
                                break

                            w, h, point = search(down, threshold)

                            if point:
                                p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                                for i in range(8):
                                    p.click()
                                    sleep(0.3)

                                sleep(waitAction)

                            else:
                                print("Error: {} not found. Where am I?".format(down))
                                phase = 3
                                break

                # CONFIRM QUIT BUTTON
                elif phase == 7:
                    w, h, point = search(leave, threshold)

                    if point:
                        p.moveTo(point[0][0] + w // 2, point[0][1] + h // 2)
                        p.click()
                        sleep(waitAction)
                        p.press("esc")
                        sleep(waitAction)
                        p.press("esc")
                        sleep(waitAction)
                        phase = 0
                    else:
                        missingCount += 1
                        print("{} not found: {}".format(leave, missingCount))
                        if missingCount > 3:
                            missingCount = 0
                            print("Error: {} not found. Where am I? Quit".format(leave))
                            p.press("esc")
                            sleep(waitAction)
                            p.press("esc")
                            sleep(waitAction)
                            phase = 3

                else:
                    break

    except p.FailSafeException:
        print("Fail-Safe triggered. Stopping")
    except Exception as e:
        print("Fatal error: {}".format(e))
        message = "Error `{}`. Quit".format(e)
        if telegramToken and telegramID:
            try:
                res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(telegramToken, telegramID, urllib.parse.quote_plus(message)))
            except Exception as e:
                print(e)

    message = "Data\n\tTotal time: {:.2f}s\n\tTotal assists: {} players\n\tEstimated GB's projects: {} projects\n\tTotal guilds: {} guilds\nOther\n\tAssist/sec: {:.2f}a/s\n\t% project/assist: {:.2f}%\n\tPlayers/guild: {:.2f}p/g".format(time.time() - ts, assistCount, projectsCount, guildCount, assistCount / (time.time() - ts), 100 / (assistCount / projectsCount) if projectsCount > 0 else 0, assistCount / guildCount if guildCount > 0 else 0)

    if telegramToken and telegramID:
        try:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(telegramToken, telegramID, urllib.parse.quote_plus(message)))
        except Exception as e:
            print(e)

    TOTAL[0] += int(time.time() - ts)
    TOTAL[1] += assistCount
    TOTAL[2] += guildCount
    TOTAL[3] += projectsCount
    TOTAL[4] += reloadCount

    with open("Data.csv", "w") as _F:
        _F.write("#Automatically generated by {}\n[Total]\n#Time,Assists,Guilds,Projects,Reloads\n{},{},{},{},{}\n[Sessions]\n#From,To,Assists,Guilds,Projects,Reloads\n".format(FILE_NAME, *TOTAL))
        for session in SESSIONS:
            _F.write(session + "\n")
        _F.write("{},{},{},{},{},{}\n".format(str(datetime.fromtimestamp(ts))[:-7], str(datetime.now())[:-7], assistCount, guildCount, projectsCount, reloadCount))

    input("\n{}\nPress [ENTER] to continue".format(message))
