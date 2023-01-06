#!/bin/python3
#-*- coding: utf-8 -*-

#
# Modules to import
#
import sqlite3

#
# Global var
#
db = sqlite3.connect("HSK.db")
db.text_factory = str
cursor = db.cursor()

#
# User functions
#
def check_vocabulary():
	request = "SELECT * FROM Vocabulary"
	cursor.execute(request)
	print(cursor.fetchall())

def check_definition():
	request = "SELECT * FROM Definition"
	cursor.execute(request)
	print(cursor.fetchall())

def check_example():
	request = "SELECT * FROM Example"
	cursor.execute(request)
	print(cursor.fetchall())

def check_wordExample():
	request = "SELECT * FROM WordExample"
	cursor.execute(request)
	print(cursor.fetchall())

def check_character():
	request = "SELECT * FROM Character"
	cursor.execute(request)
	print(cursor.fetchall())

def check_classifier():
	request = "SELECT * FROM Classifier"
	cursor.execute(request)
	print(cursor.fetchall())

def check_vocDef():
	request = "SELECT * FROM VocDef"
	cursor.execute(request)
	print(cursor.fetchall())

def check_synonym():
	request = "SELECT * FROM Synonym"
	cursor.execute(request)
	print(cursor.fetchall())

def main():
	#check_vocabulary()
	#check_definition()
	#check_example()
	#check_wordExample()
	check_character()
	#check_classifier()
	#check_vocDef()
	#check_synonym()

#
# Main function
#
if __name__ == "__main__":
	main()
