#!/bin/python3
import sqlite3
import csv
import re

def addDefinition(definition, vocId):
	if (definition[:3] == "CL:"):
		definition = definition[3:]
		# print(definition)
		# print("Classifier !")
		classifiers = definition.split(',')
		for classifier in classifiers:
			addClassifier(classifier, vocId)		
		return
	try:
		request = f"INSERT INTO Definition(definition)\
		VALUES ('{definition}')"
		# print(request)
		cursor.execute(request)
		request = "SELECT last_insert_rowid()"
		cursor.execute(request)
		defId = cursor.fetchall()[0][0]
	except Exception:
		# print(definition, "déjà existant")
		request = f"SELECT defId\
		FROM Definition\
		WHERE definition = '{definition}'"
		cursor.execute(request)
		defId = cursor.fetchall()[0][0]

	# Add definition to new word
	try:
		request = f"INSERT INTO VocDef (vocId, defId)\
		VALUES ('{vocId}', '{defId}')"
		cursor.execute(request)
	except Exception:
		print(definition)

	# Get the other words with the same definitions and add synonyms
	request = f"SELECT vocId\
	FROM VocDef\
	WHERE defId = '{defId}'"
	cursor.execute(request)
	response = cursor.fetchall()
	# print(response)
	for voc in response:
		vocId2 = voc[0]
		if (vocId2 != vocId):
			request = f"INSERT INTO Synonym (word1, word2)\
			VALUES('{vocId}', '{vocId2}')"

def addClassifier(classifier, vocId):
	pinyin = classifier[classifier.find('[')+1:classifier.find(']')]
	characters = classifier[:classifier.find('[')].split('|')
	traditional = characters[0]
	if (len(characters) == 2):
		simplified = characters[1]
	else:
		simplified = traditional
	# print(pinyin, simplified, traditional)
	try:
		request = f"INSERT INTO Classifier\
		(simplified, traditional, pinyin)\
		VALUES('{simplified}', '{traditional}', '{pinyin}')"
		# print(request)
		cursor.execute(request)
	except Exception:
		# print("déjà le classificateur dedans")
		pass
	request = f"SELECT clId\
	FROM Classifier\
	WHERE traditional = traditional\
	AND pinyin = pinyin\
	AND simplified = simplified"
	cursor.execute(request)
	clId = cursor.fetchall()[0]
	request = f"INSERT INTO VocClassifier (vocId, clId)\
	VALUES ('{vocId}', '{clId}')"
	# print(request)
	cursor.execute(request)

def escapeChars(string):
	if string is None:
		return None
	return string.strip().replace("'", "''").replace('"', '""')

def addVocabulary(simplified, traditional, pinyin, hsk, weight):
	request = f"INSERT INTO Vocabulary\
	(simplified, traditional, pinyin, hsk, weight)\
	VALUES ('{simplified}', '{traditional}', '{pinyin}', '{hsk}', '{weight}')"
	# print(request)
	cursor.execute(request)
	

# Create the database
db = sqlite3.connect("HSK.db")
db.text_factory = str
cursor = db.cursor()

def main():
	with open("data/hsk.csv") as csvfile:
		reader = csv.DictReader(csvfile, delimiter='@')
		for row in reader:
			#vocId = row['hskId']
			simplified = escapeChars(row['simplified'])
			traditional = escapeChars(row['traditional'])
			pinyin = escapeChars(row['pinyin'])
			#definitions = row['definitions'].split('/')
			definitions = re.split('/;', row['definitions'])
			hsk = row['hsk']
			example = escapeChars(row['example'])
			exampleTranslation = escapeChars(row['exampleTranslation'])
			weight = row['weight']
			addVocabulary(simplified, traditional, pinyin, hsk, weight)
			request = "SELECT last_insert_rowid()"
			cursor.execute(request)
			vocId = cursor.fetchall()[0][0]
			for definition in definitions:
				definition = escapeChars(definition)
				addDefinition(definition, vocId)

	# Save transactions
	db.commit()
	# Close database
	db.close()

if __name__ == "__main__":
	main()
