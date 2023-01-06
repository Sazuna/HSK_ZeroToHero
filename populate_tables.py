#!/bin/python3
import sqlite3
import csv
import re
import thulac

#
# Global var
#
db = sqlite3.connect("HSK.db")
db.text_factory = str
cursor = db.cursor()
seg = thulac.thulac(seg_only=True)

def addDefinition(definition, vocId):
	if (definition[:3] == "CL:"):
		definition = definition[3:]
		classifiers = definition.split(',')
		for classifier in classifiers:
			addClassifier(classifier, vocId)		
		return
	try:
		request = f"INSERT INTO Definition(definition)\
		VALUES ('{definition}')"
		cursor.execute(request)
		request = "SELECT last_insert_rowid()"
		cursor.execute(request)
		defId = cursor.fetchall()[0][0]
	except:
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
	except:
		pass

	# Get the other words with the same definitions and add synonyms
	request = f"SELECT vocId\
	FROM VocDef\
	WHERE defId = '{defId}'\
	AND vocId != '{vocId}'"
	cursor.execute(request)
	response = cursor.fetchall()
	for voc in response:
		vocId2 = voc[0]
		if (vocId2 != vocId):
			try:
				request = f"INSERT INTO Synonym (word1, word2)\
				VALUES('{vocId}', '{vocId2}')"
				cursor.execute(request)
				request = f"INSERT INTO Synonym (word2, word1)\
				VALUES('{vocId}', '{vocId2}')"
				cursor.execute(request)
			except:
				pass

def addExample(example, exampleTranslation):
	try:
		request = f"INSERT INTO Example (example, exampleTranslation)\
		VALUES ('{example}', '{exampleTranslation}')"
		cursor.execute(request)
		request = "SELECT last_insert_rowid()"
		cursor.execute(request)
		exId = cursor.fetchall()[0][0]
	except:
		request = f"SELECT exId FROM Example\
		WHERE example = '{example}'"
		cursor.execute(request)
		exId = cursor.fetchall()[0]
	# for each word in example
	exampleSeg = seg.cut(example, text=True)
	for word in exampleSeg.split():
		try:
			request = f"INSERT INTO WordExample (word, exId)\
			VALUES ('{word}', '{exId}')"
			cursor.execute(request)
		except:
			pass

def addClassifier(classifier, vocId):
	pinyin = classifier[classifier.find('[')+1:classifier.find(']')]
	characters = classifier[:classifier.find('[')].split('|')
	traditional = characters[0]
	if (len(characters) == 2):
		simplified = characters[1]
	else:
		simplified = traditional
	try:
		request = f"INSERT INTO Classifier\
		(simplified, traditional, pinyin)\
		VALUES('{simplified}', '{traditional}', '{pinyin}')"
		cursor.execute(request)
	except: 
		pass
	request = f"SELECT clId\
	FROM Classifier\
	WHERE traditional = '{traditional}'\
	AND pinyin = '{pinyin}'\
	AND simplified = '{simplified}'"
	cursor.execute(request)
	clId = cursor.fetchall()[0]
	request = f"INSERT INTO VocClassifier (vocId, clId)\
	VALUES ('{vocId}', '{clId}')"
	cursor.execute(request)

def addVocabulary(simplified, traditional, pinyin, hsk, weight):
	request = f"INSERT INTO Vocabulary\
	(simplified, traditional, pinyin, hsk, weight)\
	VALUES ('{simplified}', '{traditional}', '{pinyin}', '{hsk}', '{weight}')"
	cursor.execute(request)
	request = "SELECT last_insert_rowid()"
	cursor.execute(request)
	vocId = cursor.fetchall()[0][0]
	return vocId

def addCharacter(simplified, traditional):
	try:
		request = f"INSERT INTO Character\
		(simplified, traditional)\
		VALUES ('{simplified}', '{traditional}')"
		cursor.execute(request)
	except:
		pass # Already in

def escapeChars(string):
	if string is None:
		return None
	return string.strip().replace("'", "''").replace('"', '""')

def main():
	with open("data/hsk.csv") as csvfile:
		reader = csv.DictReader(csvfile, delimiter='@')
		for row in reader:
			simplified = escapeChars(row['simplified'])
			traditional = escapeChars(row['traditional'])
			pinyin = escapeChars(row['pinyin'])
			definitions = re.split('/|;', row['definitions'])
			hsk = row['hsk']
			example = escapeChars(row['example'])
			exampleTranslation = escapeChars(row['exampleTranslation'])
			weight = row['weight']
			vocId = addVocabulary(simplified, traditional, pinyin, hsk, weight)
			for definition in definitions:
				definition = escapeChars(definition)
				addDefinition(definition, vocId)

			for idx, sim in enumerate(simplified):
				trad = traditional[idx]
				addCharacter(sim, trad)

			if example is not None:
				addExample(example, exampleTranslation)

	# Save transactions
	db.commit()
	# Close database
	db.close()

if __name__ == "__main__":
	main()
