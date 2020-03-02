try:
	import time, cv2, mss, numpy as np, pyautogui as p
except Exception as e:
	print("Missing lib: {}. Quit".format(e))
	exit()
	
def sleep():
	time.sleep(1)

def search(name):
	print("Looking for: {}".format(name))
	template = cv2.imread(name)
	capture = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_RGBA2RGB)
	res = cv2.matchTemplate(capture, template, cv2.TM_CCOEFF_NORMED)
	return (len(template[0]), len(template), list(zip(*np.where(res >= threshold)[::-1])))

if input("1) Log into your FoE's account\n2) Keep the window visible\n3) Run it\nIf you want to stop the script, just move the cursor in the top left corner of your monitor.\nUnderstand? (y/N)").lower() != "y":
	exit()

tabs = {0: "GuildTab.PNG", 1: "FriendsTab.PNG"}
buttons = {0: "First.PNG", 1: "Next.PNG"}
assist = "Assist.PNG"
threshold = 0.91

tab = 0
countMissing = 0
assistCount = 0
ts = time.time()

with mss.mss() as sct:
	monitor = sct.monitors[0]

	while tab in tabs:
		w, h, point = search(tabs[tab])

		if point:
			p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
			p.click()
			sleep()
			button = 0

			while "Looking for buttons":
				if countMissing > 3:
					countMissing = 0
					break

				w, h, point = search(buttons[button])

				if point:
					if button == 0:
						button = 1

					p.moveTo(point[0][0] + w//2, point[0][1] + h//2)
					p.click()
					sleep()

					while "Looking for assists":
						w, h, points = search(assist)

						if points:
							countMissing = 0
							for point in points:
								p.moveTo(point[0] + w//2, point[1] + h//2)
								p.click()
								assistCount += 1
								sleep()
						else:
							print("{} not found".format(assist))
							countMissing += 1
							break
				else:
					print("Error: {} not found".format(buttons[button]))
					exit()
		else:
			print("{} not found".format(tabs[tab]))
		
		tab += 1

input("\nResults:\nTotal time: {:.2f}s\nTotal assist: {} players\nPress [ENTER] to continue".format(time.time() - ts, assistCount))
