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
def view_vocabulary(word):
	request = f"SELECT vocId, simplified, traditional, pinyin, hsk\
	FROM Vocabulary\
	WHERE simplified = '{word}' OR traditional = '{word}'"
	cursor.execute(request)
	response = cursor.fetchall()
	for word in response:
		print("simplified: ", word[1])
		print("traditional: ", word[2])
		print("pinyin: ", word[3])
		print("hsk level: ", word[4])
		vocId = word[0]
		request = f"SELECT definition\
		FROM Definition\
		INNER JOIN VocDef\
		ON Definition.defId = VocDef.defId\
		INNER JOIN Vocabulary\
		ON Vocabulary.vocId = VocDef.vocId\
		WHERE VocDef.vocId = '{vocId}'"
		cursor.execute(request)
		definitions = cursor.fetchall()
		for definition in definitions:
			print("Definition:", definition[0])

def main(word):
	view_vocabulary(word)
#
# Main function
#
if __name__ == "__main__":
	if len(sys.argv) < 2:
		exit
	main(sys.argv[1])
