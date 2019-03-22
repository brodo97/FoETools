import json, time, os, platform, shutil, operator
from datetime import datetime, timedelta

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

weekDays = {"Lun": 0,
			"Mar": 1,
			"Mer": 2,
			"Gio": 3,
			"Ven": 4,
			"Sab": 5,
			"Dom": 6}

def getEventDate(event):
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
	date = datetime.fromtimestamp(time.time()) + timedelta(days=offDays, hours=offHours, minutes=offMinutes)

	return "{yyyy}/{mm}/{dd}_{hh}:{mi}".format(yyyy=date.year, mm=date.month, dd=date.day, hh=date.hour, mi=date.minute)


data = None
terminalWidth = shutil.get_terminal_size().columns
players = {}
valid = 1

if "MotivatorsHistory.csv" in os.listdir("."):
	with open("MotivatorsHistory.csv", "r") as file:
		for line in file:
			agrs = line.rstrip("\n").split(",")
			players[agrs[0]] = agrs[1:]

try:
	with open([file for file in os.listdir(".") if ".har" in file][0], "r") as file:
		data = json.loads(file.read())
	valid = 1
except Exception as e:
	pass

dashWidth = 0

if valid and data:
	for entry in data["log"]["entries"]:
		for header in entry["response"]["headers"]:
			if header["name"] == "content-type" and header["value"] == "application/json":
				for line in json.loads(entry["response"]["content"]["text"]):
					if "responseData" in line and type(line["responseData"]) == type({}) and "events" in line["responseData"]:
						for evento in line["responseData"]["events"]:
							if "interaction_type" in evento and evento["interaction_type"] in ["motivate", "polivate_failed"]:
								eventDate = getEventDate(evento["date"])
								if evento["other_player"]["name"] not in players:
									players[evento["other_player"]["name"]] = [eventDate]
								else:
									if eventDate not in players[evento["other_player"]["name"]]:
										players[evento["other_player"]["name"]].append(eventDate)

								if len(evento["other_player"]["name"]) + len(players[evento["other_player"]["name"]]) + 7 > dashWidth:
									dashWidth = len(evento["other_player"]["name"]) + len(players[evento["other_player"]["name"]]) + 5

clear()

longestName = max([len(nome) for nome in players])
countPerPlayer = {name:len(players[name]) for name in players}

centerPrint("#" * dashWidth, terminalWidth)

for name in reversed(sorted(countPerPlayer.items(), key=operator.itemgetter(1))):
	centerPrint("{0: <{space}}: {1}".format(name[0], len(players[name[0]]), space=longestName), terminalWidth)

centerPrint("#" * dashWidth, terminalWidth)

if valid and data:
	with open("MotivatorsHistory.csv", "w") as file:
		for name in players:
			file.write("{},{}\n".format(name, ",".join(players[name])))

input()
