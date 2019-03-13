import json, pyperclip, time, os, platform, shutil
from datetime import datetime, timedelta

weekDays = {"Lun": 0,
			"Mar": 1,
			"Mer": 2,
			"Gio": 3,
			"Ven": 4,
			"Sab": 5,
			"Dom": 6}

if platform.system() == "Windows":
	clear = lambda: os.system("cls")
else:
	clear = lambda: os.system("clear")

def centerPrint(sentence, width):
	if len(sentence) <= width - 2:
		print(sentence.center(width))
	else:
		words = sentence.split(" ")
		for x in range(1,len(words)):
			if len(" ".join(words[:x+1])) > width - 2:
				print(" ".join(words[:x]).center(width))
				centerPrint(" ".join(words[x:]), width)
				return
	return

def getEventTimestamp(event):
	offDays = 0
	offHours = 0
	offMinutes = 0

	eventDay = event[:3]
	eventHour = int(event.split(":")[0][-2:])
	eventMinute = int(event.split(":")[1])

	weekdayNow = datetime.today().weekday()
	hourNow = datetime.today().hour
	minuteNow = datetime.today().minute

	if eventDay == "ier":
		offDays = -1
	elif eventDay != "ogg":
		if weekdayNow > weekDays[eventDay]:
			offDays = - (weekdayNow - weekDays[eventDay])
		elif weekdayNow < weekDays[eventDay]:
			offDays = - (7 + weekdayNow - weekDays[eventDay])
		elif weekdayNow == weekDays[eventDay]:
			offDays = -7

	offHours = eventHour - hourNow
	offMinutes = eventMinute - minuteNow 

	return datetime.timestamp(datetime.fromtimestamp(time.time()) + timedelta(days=offDays, hours=offHours, minutes=offMinutes))

terminalWidth =  shutil.get_terminal_size().columns
prev = ""
players = {}
intro = "Waiting for valid data"
introLen = len(intro)
clear()

centerPrint("#" * int(introLen + 6), terminalWidth)
centerPrint("#{}#".format(" " * int(introLen + 4)), terminalWidth)
centerPrint("#  {}  #".format(intro), terminalWidth)
centerPrint("#{}#".format(" " * int(introLen + 4)), terminalWidth)
centerPrint("#" * int(introLen + 6), terminalWidth)

while True:
	#Is data changed?
	if pyperclip.paste() != prev:
		prev = pyperclip.paste()
		valid = 0
		try:
			#Is data a valid JSON?
			data = json.loads(pyperclip.paste())
			valid = 1
		except Exception as e:
			pass

		if valid:
			#Do the magic
			for line in data:
				if "responseData" in line and type(line["responseData"]) == type({}) and "events" in line["responseData"]:
					for evento in line["responseData"]["events"]:
						if "interaction_type" in evento and evento["interaction_type"] in ["motivate", "polivate_failed"]:
							if evento["other_player"]["name"] not in players:
								eventTimestamp = getEventTimestamp(evento["date"])
								players[evento["other_player"]["name"]] = [[eventTimestamp], 1]
							else:
								if evento["date"] not in players[evento["other_player"]["name"]][0]:
									players[evento["other_player"]["name"]][1] += 1

					clear()

					longestName = max([len(nome) for nome in players]) + 1

					centerPrint("#" * int(longestName + 8), terminalWidth)

					for name in players:
						centerPrint("#  {0: <{space}}: {1}  #".format(name, players[name][1], space=longestName), terminalWidth)

					centerPrint("#" * int(longestName + 8), terminalWidth)
	time.sleep(1)
