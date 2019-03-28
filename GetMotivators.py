import json, time, os, platform, shutil, operator
from datetime import datetime as dt, timedelta
from pprint import pprint

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
friends = {}
neighbors = {}
guilds = {}
valid = 1

if "MotivatorsHistory - Friends.csv" in os.listdir("."):
	with open("MotivatorsHistory - Friends.csv", "r") as file:
		for line in file:
			agrs = line.rstrip("\n").split(",")
			friends[agrs[0]] = agrs[1:]

if "MotivatorsHistory - Neighbors.csv" in os.listdir("."):
	with open("MotivatorsHistory - Neighbors.csv", "r") as file:
		for line in file:
			agrs = line.rstrip("\n").split(",")
			neighbors[agrs[0]] = agrs[1:]

if "MotivatorsHistory - Guilds.csv" in os.listdir("."):
	with open("MotivatorsHistory - Guilds.csv", "r") as file:
		for line in file:
			agrs = line.rstrip("\n").split(",")
			guilds[agrs[0]] = agrs[1:]

har_files = []
for file_name in list(filter(lambda name: "har" in name, os.listdir("."))):
	try:
		with open([file for file in os.listdir(".") if ".har" in file][0], "r") as file:
			data = json.loads(file.read())
		
		har_files.append(data)
		valid = 1
	except Exception as e:
		pass

if valid and data:
	for data in har_files:
		for entry in data["log"]["entries"]:
			for header in entry["response"]["headers"]:
				if header["name"] == "content-type" and header["value"] == "application/json":
					for line in json.loads(entry["response"]["content"]["text"]):
						if "responseData" in line and type(line["responseData"]) == type({}) and "events" in line["responseData"]:
							for evento in line["responseData"]["events"]:
								if "interaction_type" in evento and evento["interaction_type"] in ["motivate", "polivate_failed"]:
									eventDate = getEventDate(evento["date"])

									if evento["other_player"]["is_friend"]:
										if evento["other_player"]["name"] not in friends:
											friends[evento["other_player"]["name"]] = [eventDate]
										else:
											if eventDate not in friends[evento["other_player"]["name"]]:
												friends[evento["other_player"]["name"]].append(eventDate)

									if evento["other_player"]["is_neighbor"]:
										if evento["other_player"]["name"] not in neighbors:
											neighbors[evento["other_player"]["name"]] = [eventDate]
										else:
											if eventDate not in neighbors[evento["other_player"]["name"]]:
												neighbors[evento["other_player"]["name"]].append(eventDate)

									if evento["other_player"]["is_guild_member"]:
										if evento["other_player"]["name"] not in guilds:
											guilds[evento["other_player"]["name"]] = [eventDate]
										else:
											if eventDate not in guilds[evento["other_player"]["name"]]:
												guilds[evento["other_player"]["name"]].append(eventDate)
clear()

longest_friend_name = max([len(nome) for nome in friends])
count_x_player_friends = {name:len(friends[name]) for name in friends}

longest_neighbor_name = max([len(nome) for nome in neighbors])
count_x_player_neighbor = {name:len(neighbors[name]) for name in neighbors}

longest_guild_name = max([len(nome) for nome in guilds])
count_x_player_guild= {name:len(guilds[name]) for name in guilds}

print("#"* terminalWidth)
centerPrint("FRIENDS", terminalWidth)

for name in reversed(sorted(count_x_player_friends.items(), key=operator.itemgetter(1))):
	centerPrint("{0: <{space}}: {1}".format(name[0], len(friends[name[0]]), space=longest_friend_name), terminalWidth)

print("#"* terminalWidth)

centerPrint("NEIGHBORS", terminalWidth)

for name in reversed(sorted(count_x_player_neighbor.items(), key=operator.itemgetter(1))):
	centerPrint("{0: <{space}}: {1}".format(name[0], len(neighbors[name[0]]), space=longest_neighbor_name), terminalWidth)

print("#"* terminalWidth)

centerPrint("GUILD", terminalWidth)

for name in reversed(sorted(count_x_player_guild.items(), key=operator.itemgetter(1))):
	centerPrint("{0: <{space}}: {1}".format(name[0], len(guilds[name[0]]), space=longest_guild_name), terminalWidth)

print("#"* terminalWidth)

if valid and data:
	with open("MotivatorsHistory - Friends.csv", "w") as file:
		for name in friends:
			file.write("{},{}\n".format(name, ",".join(friends[name])))

	with open("MotivatorsHistory - Neighbors.csv", "w") as file:
		for name in neighbors:
			file.write("{},{}\n".format(name, ",".join(neighbors[name])))

	with open("MotivatorsHistory - Guilds.csv", "w") as file:
		for name in guilds:
			file.write("{},{}\n".format(name, ",".join(guilds[name])))

warn = 0

if len(set(neighbors) & set(guilds)) > 0:
	print("Neighbors and guild members:\n{}\n".format(", ".join(list(set(neighbors) & set(guilds)))))
	warn = 1

if len(set(neighbors) & set(friends)) > 0:
	print("Neighbors and friends:\n{}\n".format(", ".join(list(set(neighbors) & set(friends)))))
	warn = 1

if len(set(friends) & set(guilds)) > 0:
	print("Friends and guild members:\n{}\n".format(", ".join(list(set(friends) & set(guilds)))))
	warn = 1

total = {}
for name in friends:
	if name not in total:
		total[name] = friends[name]
	else:
		for date in friends[name]:
			if date not in total[name]:
				total[name].append(date)

for name in neighbors:
	if name not in total:
		total[name] = neighbors[name]
	else:
		for date in neighbors[name]:
			if date not in total[name]:
				total[name].append(date)

for name in guilds:
	if name not in total:
		total[name] = guilds[name]
	else:
		for date in guilds[name]:
			if date not in total[name]:
				total[name].append(date)

try:
	import numpy as np
	import matplotlib.pyplot as plt
	if warn:
		print("This may alter graphs' fidelity")
except Exception as e:
	print("'pip install matplotlib' to show the graph")
	input()
else:
	def show_heatmap():
		fig = plt.figure()
		fig.subplots_adjust(hspace=0.4, wspace=0.4)
		ax = fig.add_subplot(2, 2, 1)
		calendar_heatmap(ax, *generate_data(total), "autumn", "Total Assists")
		ax = fig.add_subplot(2, 2, 2)
		calendar_heatmap(ax, *generate_data(friends), "summer", "Friends' Assists")
		ax = fig.add_subplot(2, 2, 3)
		calendar_heatmap(ax, *generate_data(neighbors), "spring", "Neighbors' Assists")
		ax = fig.add_subplot(2, 2, 4)
		calendar_heatmap(ax, *generate_data(guilds), "winter", "Guild's Assists")

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

	def calendar_heatmap(ax, dates, data, color, title):
		i, j, calendar = calendar_array(dates, data)
		im = ax.imshow(calendar, interpolation='none', cmap=color)
		ax.set_title(title)
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

	def callback_left_button(event):
		print('Left button pressed')


	def callback_right_button(event):
		print('Right button pressed')

	show_heatmap()
