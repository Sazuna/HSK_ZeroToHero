#!/bin/python3
import sqlite3


# Create the database
db = sqlite3.connect("HSK.db")
db.text_factory = str
cursor = db.cursor()

# Table vocabulary
request = "CREATE TABLE Vocabulary(\
	vocId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	simplified VARCHAR(4) NOT NULL,\
	traditional VARCHAR(4) NOT NULL,\
	pinyin VARCHAR(30) NOT NULL,\
	hsk VARCHAR(1),\
	weight INTEGER)"
cursor.execute(request)

request = "CREATE TABLE Definition(\
	defId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	definition TEXT UNIQUE NOT NULL)"
cursor.execute(request)

request = "CREATE TABLE Example(\
	exId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	example TEXT NOT NULL,\
	exampleTranslation TEXT,\
	UNIQUE (example))"
cursor.execute(request)

request = "CREATE TABLE VocDef(\
	vocDefId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	vocId INTEGER NOT NULL,\
	defId INTEGER NOT NULL,\
	FOREIGN KEY (vocId)\
	REFERENCES Vocabulary(vocId),\
	FOREIGN KEY (defId)\
	REFERENCES Definition (defId),\
	UNIQUE(vocId, defId))"
cursor.execute(request)

request = "CREATE TABLE WordExample(\
	word VARCHAR(4) NOT NULL,\
	exId INTEGER NOT NULL,\
	FOREIGN KEY (exId)\
	REFERENCES Example(exId),\
	PRIMARY KEY (word, exId))"
cursor.execute(request)

request = "CREATE TABLE Character(\
	simplified CHAR(1) NOT NULL,\
	traditional CHAR(1) NOT NULL,\
	PRIMARY KEY (simplified, traditional))"
cursor.execute(request)

request = "CREATE TABLE Synonym(\
	word1 INTEGER NOT NULL,\
	word2 INTEGER NOT NULL CHECK(word1 != word2),\
	FOREIGN KEY (word1)\
	REFERENCES Vocabulary(vocId),\
	FOREIGN KEY (word2)\
	REFERENCES Vocabulary(vocId),\
	PRIMARY KEY(word1, word2))"
cursor.execute(request)

request = "CREATE TABLE Classifier(\
	clId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	simplified VARCHAR(2) NOT NULL,\
	traditional VARCHAR(2) NOT NULL,\
	pinyin VARCHAR(14) NOT NULL,\
	definition TEXT,\
	UNIQUE(simplified, traditional, pinyin))"
cursor.execute(request)

request = "CREATE TABLE VocClassifier(\
	vocId INTEGER NOT NULL,\
	clId INTEGER NOT NULL,\
	FOREIGN KEY (vocId)\
	REFERENCES Vocabulary(vocId),\
	FOREIGN KEY (clId)\
	REFERENCES Classifier(clId))"
cursor.execute(request)

request = "CREATE TABLE POS(\
	posId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	pos VARCHAR(5) NOT NULL,\
	UNIQUE(pos))"
cursor.execute(request)

request = "CREATE TABLE vocDefPOS(\
	vocDefId INTEGER NOT NULL,\
	posId INTEGER NOT NULL,\
	PRIMARY KEY (vocDefId, posId)\
	FOREIGN KEY (vocDefId)\
	REFERENCES VocDef(vocDefId),\
	FOREIGN KEY (posId)\
	REFERENCES POS(posId))"
cursor.execute(request)

# Save transactions
db.commit()
# Close database
db.close()
