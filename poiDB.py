import numpy as np

from collections import OrderedDict

'''
	Class: Table
	
	Description: 
		Tables are named, ordered dictionaries with primary keys and a
		list of its columns.
	
	Notes: 
		1 - OrderedDict is used to maintain consistency for lookups and printouts 
		as dicts are unordered.
		
		2 - Table is not a real database table, it is simply a named dictionary,
		the current implementation would not allow for tables of more than 2 columns
'''
class Table:
	def __init__(self, name, pKey, columns, data):
		'''
		@param name:	Name of the Table
		@param pKey:	Primary Key of the Table
		@param data:	The data contained in the table in dictionary form
		@param columns:	The columns of the Table
		'''
		self.name = name
		self.pKey = pKey
		self.data = data
		self.columns = columns

	# Add keys and initialize their values as an empty list
	def addKey(self, key):
		if key not in self.data.keys():
			self.data[key] = []
		else:
			print("Key already exists")

	# Remove key along with its values if it exists in the table
	def removeKey(self, key):
		if key in self.data.keys():
			del self.data[key]
		else:
			print("Could not remove, key does not exist")

	#Add a value to a key if it exists; add the key if it doesn't and add the value
	def addValToKey(self, key, value):
		if key not in self.data.keys():
			self.addKey(key)		
		if value in list(self.data[key]):
			print("Value already exists")
		else:
			self.data[key].append(value)

	#Remove value from key if key exists
	def removeValFromKey(self, key, value):
		if key not in self.data.keys():
			print("Cannot remove value from non-existant key")
			return
		if value in self.data[key]:
			del self.data[key][self.data[key].index(value)]
		else:
			print("Could not remove, the value does not exist")

	#Enables human readable object representation
	def __str__(self):
		padding = 2
		tableOutput = self.name + " Table\n"
		
		#Get a list of all keys and values in a form that can be assessed for length
		#NOTE(SLatychev): This assumes that the values in the dict are a list of lists
		keys = list(self.data.keys()) 
		values = list(val for valsLst in list(self.data.values()) for val in valsLst)
		pData = list(keys) + list(values)

		#Find the longest item in the table and set the column width to that size with padding
		if pData != []:
			colWidth = max(len(str(val))  for val in pData) + padding
		else:
			colWidth = max(len(str(col)) for col in self.columns) + padding
		
		#Collect all the items of the table into a list of lists
		items = []
		for key, value in self.data.items():
			for val in value:
				items.append(list((key, value[value.index(val)])))
		
		#Generate the column headers printout
		tableOutput += "|" + "|".join(item.center(colWidth) for item in self.columns) + "|\n"
		tableOutput += "|" + len(self.columns) * ("-" * colWidth + "|") + "\n"
		
		#Generate the table data printout
		for lst in items:	
			tableOutput += "|" + "|".join(str(item).ljust(colWidth) for item in lst) + "|\n"
		
		return tableOutput

	def __repr__(self):
		return str(self)



'''
	Class: Database
	
	Description:
		Database is a dictionary container of Tables that has Table names as 
		keys and Table objects as values.
		
	Notes:
		1 - The current implementation is meant to be used as a simple data 
		storage and retrieval system that seperates out data into clean Tables.
		
		2 - The database should be Singleton
		
		3 - Discovered a class can be forced to be a singleton by defaulting 
		one of its parameters to a mutable type (dict or list) and assigning it 
		as a field of self.
		
	Credits:
		- Alex Martelli's Borg Design Pattern:
			Found a similar principle that instead of defaulting an optional 
			parameter to a mutable type, a "private" (by convention) variable 
			is made, that is of mutable type, and is assigned as a field of self. 
			Current implementation of Database uses this principle.
'''
class Database:
	_tables = OrderedDict()
	def __init__(self):
		'''
		@params tables: shared state Dictionary of Table name : Table Object 
		'''
		self.tables = self._tables

	#Creates a new table in the database if it does not exist
	def createTable(self, tabName, tabPKey, tabCols):
		if tabName not in list(self.tables.keys()):
			self.tables[tabName] = Table(tabName, tabPKey, tabCols, OrderedDict())
		else:
			print("Table already exists")

	#Drop a table if it exists
	def dropTable(self, tabName):
		if tabName in self.tables.keys():
			print("Dropping Table: " + tabName)
			del self.tables[tabName]
			if self.tables == OrderedDict():
				print("Database Empty")
		else:
			print("Could not find Table by that name")

	#Gets all keys of specified table
	def fromTableGetKeys(self, tabName):
		return list(self.tables[tabName].data.keys())

	#Gets all values of the specified table
	def fromTableGetValues(self, tabName):
		return list(self.tables[tabName].data.values())

	#Gets values of a key in a specified table
	def fromKeyInTableGetVals(self, key, tabName):
		return list(self.tables[tabName].data[key])

	#Get all keys that have specified value in specified table
	def fromValGetKeysInTable(self, val, tabName):
		values = list(self.tables[tabName].data.values())
		keyIndices = []
		
		keyIndx = 0
		while keyIndx < len(values):
			if val in values[keyIndx]:
				keyIndices.append(keyIndx)
			keyIndx += 1
		
		allKeysWithVal = []
		for i in keyIndices:
			allKeysWithVal.append(list(self.tables[tabName].data.keys())[i]) 
		
		return allKeysWithVal

	#Destroys all tables and resets the shared state of the db to a blank OrderedDict()
	def _dropCascade(self):		
		i = 0
		tables = list(self.tables.keys())
		
		#drop all tables so they don't linger in memory
		while i < len(tables):
			print(i)
			self.dropTable(tables[i])
			i += 1
		
		#Wipes the shared state to a blank one
		self._tables = OrderedDict()


	#Enables human readable object representation
	def __str__(self):
		final = ""
		for key, value in self.tables.items():
			final += (str(value)) + "\n"
		return final

	def __repr__(self):
		return str(self)



