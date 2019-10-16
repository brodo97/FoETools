try:
	import time, cv2, mss, numpy as np, pyautogui as p, platform, os, requests, urllib
except Exception as e:
	print("Missing lib: {}. Quit".format(e))
	exit()

if platform.system() == "Windows":
	clear = lambda: os.system("cls")
else:
	clear = lambda: os.system("clear")

def sleep():
	print("\nTime passed: {:.2f}s\nAssist: {}".format(time.time()-ts, assistCount))
	time.sleep(1)

def search(name, t):
	print("Looking for: {}".format(name))
	template = cv2.imread(name)
	capture = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_RGBA2RGB)
	res = cv2.matchTemplate(capture, template, cv2.TM_CCOEFF_NORMED)
	return (len(template[0]), len(template), list(zip(*np.where(res >= t)[::-1])))

if __name__ == '__main__':
	if input("1) Log into you FoE's account\n2) Keep the window visible\n3) Run it\nIf you want to stop the script, just move the cursor in the top left corner of your monitor.\nUnderstand? (y/N)").lower() != "y":
		exit()

	botToken= ""
	enter = "EnterGuild.PNG"
	guildTab = "GuildTab.PNG"
	globalBtn = "Global.PNG"
	globalGuild = "GlobalGuild.PNG"
	members = "Members.PNG"
	quit = "QuitGuild.PNG"
	down = "Down.PNG"
	leave = "LeaveGuild.PNG"
	buttons = {0: "First.PNG", 1: "Next.PNG"}
	assist = "Assist.PNG"
	threshold = 0.91

	phase = -1
	countMissing = 0
	assistCount = 0
	projectsCount = 0
	guildCount = 0
	ts = time.time()
	error = 0

	try:
		with mss.mss() as sct:
			monitor = sct.monitors[0]
			w, h, point = search(guildTab, threshold)

			if point:
				p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
				p.click()
				sleep()
				phase = 0
			else:
				print("Error: {} not found".format(guildTab))
				error = 1

			while "Automate" and not error:

				#ENTER GUILD BUTTON
				if phase == 0:
					w, h, point = search(enter, threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep()
						p.press("esc")
						sleep()
						p.press("esc")
						sleep()
						phase = 2
						guildCount += 1
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
						sleep()
						phase = 0
					else:
						print("Error: {} not found".format(buttons[1]))
						break

				#ASSIST
				elif phase == 2:
					button = 0

					while "Looking for buttons" and not error:
						if countMissing > 3:
							countMissing = 0
							phase = 3
							break

						w, h, point = search(buttons[button], threshold)

						if point:
							if button == 0:
								button = 1

							p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
							p.click()
							sleep()

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
										sleep()
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
						sleep()
						phase = 4
					else:
						p.press("esc")
						sleep()
						countMissing += 1
						print("{} not found: {}".format(globalBtn, countMissing))
						if countMissing > 3:
							countMissing = 0
							print("Error: {} not found. Where am I? Quit".format(globalBtn))
							break

				#GLOBAL -> GUILD BUTTON
				elif phase == 4:
					w, h, point = search(globalGuild, 0.98)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep()
						phase = 5
					else:
						p.press("esc")
						sleep()
						countMissing += 1
						print("{} not found: {}".format(globalGuild, countMissing))
						if countMissing > 3:
							countMissing = 0
							print("Error: {} not found. Where am I? Quit".format(globalGuild))
							break

				#GUILD MEMBERS BUTTON
				elif phase == 5:
					w, h, point = search(members, threshold)

					if point:
						p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
						p.click()
						sleep()
						sleep()
						phase = 6
					else:
						countMissing += 1
						print("{} not found: {}".format(members, countMissing))
						if countMissing > 3:
							countMissing = 0
							print("Error: {} not found. Where am I? Quit".format(members))
							break

				#QUIT GUILD BUTTON
				elif phase == 6:
					while "Searching" and not error:
						w, h, point = search(quit, 0.99)

						if point:
							p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
							p.click()
							sleep()
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
								for i in range(9):
									p.click()
									time.sleep(0.2)
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
						sleep()
						phase = 0
						p.press("esc")
						sleep()
						p.press("esc")
						sleep()
					else:
						countMissing += 1
						print("{} not found: {}".format(leave, countMissing))
						if countMissing > 3:
							countMissing = 0
							print("Error: {} not found. Where am I? Quit".format(leave))
							p.press("esc")
							sleep()
							p.press("esc")
							sleep()
							phase = 3

				else:
					break

	except p.FailSafeException:
		print("Fail-Safe triggered. Stopping")
	except Exception as e:
		print("Fatal error: {}".format(e))

	if error:
		print("Exit on phase: {}".format(phase))
	
	if phase != -1:
		message = "Data\n\tTotal time: {:.2f}s\n\tTotal assists: {} players\n\tEstimated GB's projects: {} projects\n\tTotal guilds: {} guilds\nOther\n\tAssist/sec: {:.2f}a/s\n\t% project/assist: {:.2f}%\n\tPlayers/guild: {:.2f}p/g".format(time.time() - ts, assistCount, projectsCount, guildCount, assistCount/(time.time() - ts), 100/(assistCount/projectsCount), assistCount/guildCount)

		if botToken:
			try:
				res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id=44181058&text={}&parse_mode=Markdown".format(botToken, urllib.parse.quote_plus(message)))
			except Exception as e:
				print(e)

		input("\n{}\nPress [ENTER] to continue".format(message))