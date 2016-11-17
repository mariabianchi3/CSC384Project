import random
import copy
from collections import OrderedDict

'''
	Class: Table
	
	Description: 
		Tables are named, ordered dictionaries with primary keys and a
		list of its columns.
	
	Notes: 
		1 - OrderedDict is used to maintain consistency for lookups and printouts as dicts are
		unordered.
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
			self.AddKey(key)		
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

	#String representation of the Table
	def __str__(self):
		tableOutput = self.name + " Table\n"
		pData = list(self.data.keys()) + list(self.data.values())
		pData = [val if type(sublst) == list else sublst for sublst in pData for val in sublst]
		if pData != []:
			colWidth = max(len(str(val))  for val in pData) + 2
		else:
			colWidth = max(len(str(col)) for col in self.columns) + 2
			
		items = []
		for key, value in self.data.items():
			for val in value:
				items.append(list((key, value[value.index(val)])))
		
		tableOutput += "|" + "|".join(item.center(colWidth) for item in self.columns) + "|\n"
		tableOutput += "|" + len(self.columns) * ("-" * colWidth + "|") + "\n"
		
		for lst in items:	
			tableOutput += "|" + "|".join(str(item).center(colWidth) for item in lst) + "|\n"
		
		return tableOutput

	#Representation of the Table (Placeholder)
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
		- Alex Martelli's Borg:
			Found a similar principle that instead of defaulting an optional 
			parameter to a mutable type, a "private" (by convention) variable 
			is made, that is of mutable type, and is assigned as a field of self. 
			Current implementation of Database uses this principle.
'''
class Database:
	_tables = OrderedDict()
	def __init__(self):
		'''
		@params tables: Dictionary of Table name : Table Object 
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
			del self.tables[tabName]
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

	#Get all keys that have specificied value in specified table
	def fromValGetKeysInTable(self, val, tabName):
		values = list(self.tables[tabName].data.values())
		keyIndices = []
		
		valCount = 0
		for subValue in values:
			if val in subValue:
				keyIndices.append(valCount)
			valCount += 1
		
		allKeys = []
		for key in keyIndices:
			allKeys.append(list(self.tables[tabName].data.keys())[key]) 
		
		return allKeys

	#String representation of the Database
	def __str__(self):
		final = ""
		for key, value in self.tables.items():
			final += (str(value)) + "\n"
		return final

	#Representation of the Database (Placeholder)
	def __repr__(self):
		return str(self)



