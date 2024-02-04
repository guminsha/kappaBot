import re

string = "100d100"
pattern = re.compile("[1-100]d[1-100]")
if(pattern.search(string)):
	teste = string.split("d")

print(teste)