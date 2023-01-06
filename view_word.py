#!/bin/python3
#-*- coding: utf-8 -*-

#
# Modules to import
#
import sqlite3
import sys

#
# Global var
#
db = sqlite3.connect("HSK.db")
db.text_factory = str
cursor = db.cursor()

#
# User functions
#
def view_vocabulary(word, limit_examples=-1):
	request = f"SELECT vocId, simplified, traditional, pinyin, hsk\
	FROM Vocabulary\
	WHERE simplified = '{word}' OR traditional = '{word}'"
	cursor.execute(request)
	response = cursor.fetchall()
	for word in response:
		# Word
		print("simplified: ", word[1])
		print("traditional: ", word[2])
		print('*'*38)
		print("pinyin: ", word[3])
		print("hsk level: ", word[4])
		vocId = word[0]

		# Definitions
		request = f"SELECT definition\
		FROM Definition\
		INNER JOIN VocDef\
		ON Definition.defId = VocDef.defId\
		INNER JOIN Vocabulary\
		ON Vocabulary.vocId = VocDef.vocId\
		WHERE VocDef.vocId = '{vocId}'"
		cursor.execute(request)
		definitions = cursor.fetchall()
		print("** Definitions **")
		for definition in definitions:
			print(definition[0])

		# Examples
		request = f"SELECT example, exampleTranslation\
		FROM Example\
		INNER JOIN WordExample\
		ON Example.exId = WordExample.exId\
		WHERE word = '{word[1]}'"
		if limit_examples >= 0:
			request += f" LIMIT {limit_examples}"
		cursor.execute(request)
		examples = cursor.fetchall()
		print("** Examples **")
		for example in examples:
			print(example[0])
			print(example[1])

		# Synonyms
		request = f"SELECT V2.simplified, V2.traditional, V2.pinyin, V2.hsk\
		FROM Vocabulary AS V1\
		INNER JOIN Synonym AS S\
		ON S.word1 = V1.vocId\
		INNER JOIN Vocabulary AS V2\
		ON S.word2 = V2.vocId\
		WHERE V1.vocId = '{vocId}'"
		cursor.execute(request)
		synonyms = cursor.fetchall()
		print("** Synonyms **")
		for synonym in synonyms:
			print(synonym[0], synonym[1], synonym[2], "hsk level:", synonym[3])
		print('*'*38)

def main(word, limit_examples = -1):
	view_vocabulary(word, limit_examples)
#
# Main function
#
if __name__ == "__main__":
	if len(sys.argv) < 2:
		exit
	if len(sys.argv) == 3:
		limit_examples = int(sys.argv[2])
		main(sys.argv[1], limit_examples=limit_examples)
	else:
		main(sys.argv[1])
