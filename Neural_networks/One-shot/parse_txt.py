import sys
import re
try:
	row_n = int(sys.argv[1])
except:
	row_n = 0

file_name = r"./William Strunk Jr., E. B. White, Roger Angell - The Elements of Style, Fourth Edition (1999, Longman) - libgen.lc.txt"


with open(file_name) as file:
	text = file.read()
	#sentences = re.findall(r'\. [-;,\sa-zA-Z]{4,}(!Mr)\.', text)
	sentences = re.findall("[A-Z].*?[\.!?] ", text, re.MULTILINE | re.DOTALL)
	#sentences = [cleaned[2:] for cleaned in sentences]
	sentences = sentences[100:]
	print(len(sentences))
	print(sentences[row_n])

with open('parsed.txt', 'w') as file:
	backup = ''
	counter = 0
	for i, sentence in enumerate(sentences):
		sentence = sentence.replace("  ", " ")
		sentence = sentence.strip()
		if sentence.find("\n") != -1:
			print(sentence.find("\n"))
			continue
		if len(sentence) < 5:
			backup += sentence
			continue
		file.write(f'{counter} {backup+sentence}\n')
		backup = ''
		counter += 1
