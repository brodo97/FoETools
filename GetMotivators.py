import json
import pyperclip
import time
import os
import platform

if platform.system() == "Windows":
	clear = lambda: os.system("cls")
else:
	clear = lambda: os.system("clear")

#Terminal width
dash = 80
prev = ""
players = {}
while True:
	#Load JSON data
	if pyperclip.paste() != prev:
		try:
			data = json.loads(pyperclip.paste())
			prev = pyperclip.paste()
			for line in data:
				if "responseData" in line and type(line["responseData"]) == type({}) and "events" in line["responseData"]:
					for evento in line["responseData"]["events"]:
						if "interaction_type" in evento and evento["interaction_type"] in ["motivate", "polivate_failed"]:
							if evento["other_player"]["name"] not in players:
								print(evento["other_player"]["name"])
								players[evento["other_player"]["name"]] = [[evento["date"]], 1]
							else:
								if evento["date"] not in players[evento["other_player"]["name"]][0]:
									players[evento["other_player"]["name"]][1] += 1
					clear()
					print("Assist:")
					for name in players:
						print("\t{0: <{space}}: {1}".format(name, players[name][1], space=max([len(nome) for nome in players]) + 1))
		except Exception as e:
			pass
	time.sleep(1)
