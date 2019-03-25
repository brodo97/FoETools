import json, time, os, platform, shutil, operator
from datetime import datetime as dt, timedelta

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

	weekdayNow = dt.today().weekday()
	hourNow = dt.today().hour
	minuteNow = dt.today().minute

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
	date = dt.fromtimestamp(time.time()) + timedelta(days=offDays, hours=offHours, minutes=offMinutes)

	return "{yyyy}/{mm}/{dd}".format(yyyy=date.year, mm=date.month, dd=date.day)

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
									dashWidth = len(evento["other_player"]["name"]) + len(players[evento["other_player"]["name"]]) + 3

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

try:
	import numpy as np
	import matplotlib.pyplot as plt
except Exception as e:
	print("'pip install matplotlib' to show the graph")
	input()
else:
	def show_heatmap(dati):
		dates, data = generate_data(dati)
		fig, ax = plt.subplots(figsize=(6, 8))
		calendar_heatmap(ax, dates, data)
		plt.show()

	def generate_data(dati):
		lista_d = []
		lista_s = []
		for nome in dati:
			lista_d += [dt.strptime(giorno, "%Y/%m/%d") for giorno in dati[nome]]
			lista_s += [giorno for giorno in dati[nome]]
		num = len(set(lista_s))
		data = [lista_s.count(conto) for conto in sorted(set(lista_s), key = lambda date: dt.strptime(date, '%Y/%m/%d'))]
		start = min(lista_d)
		dates = [start + timedelta(days=i) for i in range(num)]
		return dates, data

	def calendar_array(dates, data):
		i, j = zip(*[d.isocalendar()[1:] for d in dates])
		i = np.array(i) - min(i)
		j = np.array(j) - 1
		ni = max(i) + 1

		calendar = np.nan * np.zeros((ni, 7))
		calendar[i, j] = data
		return i, j, calendar

	def calendar_heatmap(ax, dates, data):
		i, j, calendar = calendar_array(dates, data)
		im = ax.imshow(calendar, interpolation='none', cmap='summer')
		label_days(ax, dates, i, j, calendar)
		label_months(ax, dates, i, j, calendar)
		ax.figure.colorbar(im)

	def label_days(ax, dates, i, j, calendar):
		ni, nj = calendar.shape
		day_of_month = np.nan * np.zeros((ni, 7))
		day_of_month[i, j] = [d.day for d in dates]
	 
		for (i, j), day in np.ndenumerate(day_of_month):
			if np.isfinite(day):
				ax.text(j, i, int(day), ha='center', va='center')
	 
		ax.set(xticks=np.arange(7),
			   xticklabels=['M', 'T', 'W', 'R', 'F', 'S', 'S'])
		ax.xaxis.tick_top()

	def label_months(ax, dates, i, j, calendar):
		month_labels = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
								 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
		months = np.array([d.month for d in dates])
		uniq_months = sorted(set(months))
		yticks = [i[months == m].mean() for m in uniq_months]
		labels = [month_labels[m - 1] for m in uniq_months]
		ax.set(yticks=yticks)
		ax.set_yticklabels(labels, rotation=90)

	show_heatmap(players)
