#
# Forge of Empires tool for flat deposit's resources
# Usage:
#   1) Use your browser's Developer Tool to get the heaviest JSON response (For me ~60KB. Higher era may generate heavier data) named 'json?h=*session id*' and paste it in a file located in the same folder as this script.
#   2) Save the file as "data.json"
#   3) Run it!
#

import json

#Terminal width
dash = 80

#Load JSON data
with open("data.json") as f:
	data = json.load(f)

resources = None
deposits = None
raw_data = None

#Look for number of resources, which one you produce and their names
for line in data:
	if type(line["responseData"]) == type({}) and "resources" in line["responseData"] and resources == None:
		resources = {l:line["responseData"]["resources"][l] for l in line["responseData"]["resources"]}
	if type(line["responseData"]) == type({}) and "states" in line["responseData"] and deposits == None:
		deposits = [l[4:] for l in line["responseData"]["states"]]
	if type(line["responseData"]) == type([]) and len(line["responseData"]) > 100 and raw_data == None:
		raw_data = {i["id"]:[i["era"],i["name"]] for i in line["responseData"] if "era" in i and i["era"] not in "AllAgeNoAge"}
	if resources and deposits and raw_data:
		break

ref_data = {}

#Join data in a more manageable structure
for name in raw_data:
	age = raw_data[ name ][0]
	nameID = raw_data[ name ][1]
	
	if age in ref_data:
		if name not in resources:
			ref_data[ age ].update({name: (nameID, 0)})
		else:
			ref_data[ age ].update({name: (nameID, resources[ name ])})
	else:
		if name not in resources:
			ref_data[ age ] = {name: (nameID, 0)} 
		else:
			ref_data[ age ] = {name: (nameID, resources[ name ])}

#Start flattering deposits
for age in ref_data:
	check = 0
	for name in ref_data[ age ]:
		check += ref_data[ age ][ name ][1]
		
	if check==0:
		continue

	print(age,"\n")
	depList = {}
	res = {}
	for name in ref_data[ age ]:
		if name in deposits:
			print("\t{:<23}: {} *".format(ref_data[ age ][ name ][0], ref_data[ age ][ name ][1]))
			depList[ref_data[ age ][ name ][0]] = ref_data[ age ][ name ][1]
		else:
			print("\t{:<23}: {}".format(ref_data[ age ][ name ][0], ref_data[ age ][ name ][1]))
			res[ref_data[ age ][ name ][0]] = ref_data[ age ][ name ][1]

	print("\n\n")

	if len(depList) != 2:
		print("Impossible to balance\n\n", "-" * dash)
		continue

	avg = ( sum(depList.values()) + sum(res.values()) ) / 5
	dep1, dep2 = avg-depList[list(depList.keys())[0]], avg-depList[list(depList.keys())[1]]
	res3, res4, res5 = avg-res[list(res.keys())[0]], avg-res[list(res.keys())[1]], avg-res[list(res.keys())[2]]

	if dep1 > 0 or dep2 > 0:
		print("Impossible to balance\n\n","-"*dash)
		continue

	print("Balance\n")

	ratio1 = 100 / -(dep1 + dep2) * -dep1
	ratio2 = 100 / -(dep1 + dep2) * -dep2

	tradeD1R3 = int(ratio1 / 100 * res3)
	tradeD1R4 = int(ratio1 / 100 * res4)
	tradeD1R5 = int(ratio1 / 100 * res5)
	tradeD2R3 = int(ratio2 / 100 * res3)
	tradeD2R4 = int(ratio2 / 100 * res4)
	tradeD2R5 = int(ratio2 / 100 * res5)

	print("{:>20}{:>23}{:>23}".format(*list(res.keys())))
	print("{:>10}{:>10}{:>23}{:>23}".format(list(depList.keys())[0], tradeD1R3, tradeD1R4, tradeD1R5))
	print("{:>10}{:>10}{:>23}{:>23}\n\n{}".format(list(depList.keys())[1], tradeD2R3, tradeD2R4, tradeD2R5, "-"*dash))
