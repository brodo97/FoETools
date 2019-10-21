try:
	import time, cv2, mss, numpy as np, pyautogui as p, os, requests, urllib, yaml
except Exception as e:
	print("Missing lib: {}. Quit".format(e))
	exit()

class ReadImage:
    def __init__(self, name):
        self.data = cv2.imread(name)
        self.__name = name

    def __str__(self):
        return self.__name

def sleep(waitTime):
	print("\nTime passed: {:.2f}s\nAssist: {}".format(time.time()-ts, assistCount))
	time.sleep(waitTime)

def search(image, t):
	print("Looking for: {}".format(image))
	template = image.data
	capture = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_RGBA2RGB)
	res = cv2.matchTemplate(capture, template, cv2.TM_CCOEFF_NORMED)
	return (len(template[0]), len(template), list(zip(*np.where(res >= t)[::-1])))

if __name__ == '__main__':
	if input("1) Log into you FoE's account\n2) Keep the window visible\n3) Run it\nIf you want to stop the script, just move the cursor in the top left corner of your monitor.\nUnderstand? (y/N)").lower() != "y":
		exit()

	if "Settings.yml" not in os.listdir("."):
		open("Settings.yml", "w").write("#Settings\n#Buttons\nenter: EnterGuild.PNG\nguildTab: GuildTab.PNG\nfriendsTab: FriendsTab.PNG\nneighborsTab: NeighborsTab.PNG\nglobalBtn: Global.PNG\nglobalGuild: GlobalGuild.PNG\nmembers: Members.PNG\nquit: QuitGuild.PNG\ndown: Down.PNG\nleave: LeaveGuild.PNG\nbutton0: First.PNG\nbutton1: Next.PNG\nassist: Assist.PNG\nexit: Exit.PNG\n#Template matching threshold\nthreshold: 0.91\n#Starting phase\nphase: -1\n#Wait times in seconds\nwaitAction: 1\nwaitAssist: 1.5\nwaitReload: 10\nmaxTimeNoAssists: 60\n#Telegram\ntelegramID:\ntelegramToken:")
	
	with open("Settings.yml") as _F:
		try:
			settings = yaml.load(_F, Loader=yaml.FullLoader)
		except:
			try:
				settings = yaml.load(_F)
			except:
				print("Can't read Settings.yml. Quit")
				exit()
		

	enter = ReadImage(settings["enter"])
	guildTab = ReadImage(settings["guildTab"]) 
	friendsTab = ReadImage(settings["friendsTab"]) 
	neighborsTab = ReadImage(settings["neighborsTab"]) 
	globalBtn = ReadImage(settings["globalBtn"])
	globalGuild = ReadImage(settings["globalGuild"])
	members = ReadImage(settings["members"])
	quit = ReadImage(settings["quit"])
	down = ReadImage(settings["down"])
	leave = ReadImage(settings["leave"])
	buttons = {0: ReadImage(settings["button0"]), 1: ReadImage(settings["button1"])}
	assist = ReadImage(settings["assist"])
	exit = ReadImage(settings["exit"])

	threshold = settings["threshold"]
	phase = settings["phase"]

	waitAction = settings["waitAction"]
	waitAssist = settings["waitAssist"]
	waitReload = settings["waitReload"]
	maxTimeNoAssists = settings["maxTimeNoAssists"]

	telegramID = settings["telegramID"]
	telegramToken = settings["telegramToken"]

	countMissing = 0
	assistCount = 0
	projectsCount = 0
	guildCount = 0
	ts = time.time()
	lastAssist = time.time()
	error = 0
	errorCount = 0
	phasesList = []

	try:
		with mss.mss() as sct:
			monitor = sct.monitors[0]
			
			if input("Assist neighbors and friends? (y/N): ").lower() == "y":
				tabs = {0: ReadImage(settings["friendsTab"]), 1: ReadImage(settings["neighborsTab"])}
				buttons = {0: ReadImage(settings["button0"]), 1: ReadImage(settings["button1"])}
				tab = 0

				while tab in tabs and not error:
					w, h, point = search(tabs[tab], threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep(waitAction)
						button = 0

						while "Looking for buttons":
							if countMissing > 3:
								countMissing = 0
								break

							w, h, point = search(buttons[button], threshold)

							if point:
								if button == 0:
									button = 1

								p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
								p.click()
								sleep(waitAssist)

								while "Looking for assists":
									w, h, points = search(assist, threshold)

									if points:
										countMissing = 0
										for point in points:
											p.moveTo(point[0] + w//2, point[1] + h//2)
											p.click()
											assistCount += 1
											sleep(waitAction)
									else:
										print("{} not found".format(assist))
										countMissing += 1
										break
							else:
								print("Error: {} not found".format(buttons[button]))
								error = 1
								break
					else:
						print("{} not found".format(tabs[tab]))
					
					tab += 1

			lastAssist = time.time()
			error = 0

			while "Automate" and not error:
				phasesList.append(phase)

				if time.time() - lastAssist > maxTimeNoAssists:
					print("No assist in the last {} seconds. Reloading".format(maxTimeNoAssists))
					p.press("f5")
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
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep(waitAction)
						phase = 0

						w, h, point = search(buttons[0], threshold)

						if point:
							p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
							p.click()
							sleep(waitAction)
						else:
							print("{} not found. What's happening?".format(buttons[0]))

					else:
						print("{} not found".format(guildTab))
						w, h, point = search(exit, threshold)

						if point:
							p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
							p.click()
							sleep(waitAction)
							phase = 0
						else:
							print("{} not found".format(exit))

							p.press("esc")
							sleep(waitAction)
							p.press("esc")

				#ENTER GUILD BUTTON
				elif phase == 0:
					w, h, point = search(enter, threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep(waitAction)
						p.press("esc")
						sleep(waitAction)
						p.press("esc")
						sleep(waitAction)
						phase = 2
						guildCount += 1
						countMissing = 0
					else:
						w, h, points = search(assist, threshold)

						if points:
							phase = 2
						else:
							phase = 1

				#NEXT GUILDS PAGE BUTTON
				elif phase == 1:
					w, h, point = search(buttons[1], threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep(waitAction)
						phase = 0
						countMissing += 1
						print("{} not found: {}".format(enter, countMissing))
						if countMissing > 3:
							countMissing = 0
							phase = 3
					else:
						print("Error: {} not found".format(buttons[1]))
						break

				#ASSIST
				elif phase == 2:
					button = 0

					while "Looking for buttons" and not error:
						if countMissing > 1:
							countMissing = 0
							phase = 3
							break

						w, h, point = search(buttons[button], threshold)

						if point:
							if button == 0:
								button = 1

							p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
							p.click()
							sleep(waitAssist)

							cycle = 0
							while "Looking for assists":
								w, h, points = search(assist, threshold)

								if points:
									if countMissing == 0 and cycle:
										projectsCount += 1
									countMissing = 0
									for point in points:
										p.moveTo(point[0] + w//2, point[1] + h//2)
										p.click()
										assistCount += 1
										lastAssist = time.time()
										sleep(waitAction)
										cycle = 1
								else:
									cycle = 0
									countMissing += 1
									print("{} not found: {}".format(assist, countMissing))
									break
						else:
							print("Error: {} not found".format(buttons[button]))
							error = 1

				#GLOBAL BUTTON
				elif phase == 3:
					w, h, point = search(enter, threshold)

					if point:
						phase = 0
						continue

					w, h, point = search(globalBtn, threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
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

				#GLOBAL -> GUILD BUTTON
				elif phase == 4:
					w, h, point = search(globalGuild, 0.98)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep(waitAction)
						phase = 5
					else:
						p.press("esc")
						sleep(waitAction)
						countMissing += 1
						print("{} not found: {}".format(globalGuild, countMissing))
						if countMissing > 3:
							countMissing = 0
							print("{} not found. Where am I?".format(globalGuild))
							phase = 3

				#GUILD MEMBERS BUTTON
				elif phase == 5:
					w, h, point = search(members, threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep(waitAction*2)
						phase = 6
					else:
						print("{} not found: {}".format(members, countMissing))

				#QUIT GUILD BUTTON
				elif phase == 6:
					while "Searching" and not error:
						w, h, point = search(quit, 0.99)

						if point:
							p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
							p.click()
							sleep(waitAction)
							phase = 7
							break
						else:
							countMissing += 1
							print("{} not found: {}".format(quit, countMissing))
							if countMissing > 12:
								countMissing = 0
								print("Error: {} not found. Where am I?".format(quit))
								phase = 3
								break

							w, h, point = search(down, threshold)

							if point:
								p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
								for i in range(8):
									p.click()
									sleep(0.3)
								
								sleep(waitAction)

							else:
								print("Error: {} not found. Where am I?".format(down))
								phase = 3
								break

				#CONFIRM QUIT BUTTON
				elif phase == 7:
					w, h, point = search(leave, threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep(waitAction)
						phase = 0
						p.press("esc")
						sleep(waitAction)
						p.press("esc")
						sleep(waitAction)
					else:
						countMissing += 1
						print("{} not found: {}".format(leave, countMissing))
						if countMissing > 3:
							countMissing = 0
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

	if error:
		print("Exit on phase: {}".format(phase))
	
	if phase != -1:
		message = "Data\n\tTotal time: {:.2f}s\n\tTotal assists: {} players\n\tEstimated GB's projects: {} projects\n\tTotal guilds: {} guilds\nOther\n\tAssist/sec: {:.2f}a/s\n\t% project/assist: {:.2f}%\n\tPlayers/guild: {:.2f}p/g".format(time.time() - ts, assistCount, projectsCount, guildCount, assistCount/(time.time() - ts), 100/(assistCount/projectsCount) if projectsCount > 0 else 0, assistCount/guildCount if guildCount > 0 else 0)

		if telegramToken and telegramID:
			try:
				res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(telegramToken, telegramID, urllib.parse.quote_plus(message)))
			except Exception as e:
				print(e)

	input("\n{}\nPress [ENTER] to continue".format(message))