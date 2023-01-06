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
def view_characters():
	request = f"SELECT simplified, traditional\
	FROM Character"
	cursor.execute(request)
	response = cursor.fetchall()
	for character in response:
		print("simplified: ", character[0], "; traditional: ", character[1])

def main():
	view_characters()
#
# Main function
#
if __name__ == "__main__":
	main()
