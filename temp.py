with open('temp.txt') as file:
	final = []
	for line in file:
		for x in line.split(" / "):
			final.append(x)

print(final)